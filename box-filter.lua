-- box-filter.lua
-- Pandoc Lua filter for Proving Nothing
-- Handles: Part dividers, epigraphs, styled boxes, horizontal rules.
-- Design pass: suppresses redundant HRs adjacent to headings/parts.

-- Map div classes to LaTeX environments
local box_map = {
  technical  = "technicalbox",
  insight    = "insightbox",
  caution    = "cautionbox",
  example    = "examplebox",
  -- Legacy aliases for backward compatibility
  patient    = "insightbox",
  regulatory = "examplebox",
}

-- Handle fenced divs: ::: {.technical} ... :::
function Div(el)
  for cls, env in pairs(box_map) do
    if el.classes:includes(cls) then
      local blocks = {}
      table.insert(blocks, pandoc.RawBlock("latex", "\\begin{" .. env .. "}"))
      for _, b in ipairs(el.content) do
        table.insert(blocks, b)
      end
      table.insert(blocks, pandoc.RawBlock("latex", "\\end{" .. env .. "}"))
      return blocks
    end
  end
end

-- Handle blockquotes: epigraphs and Technical Detail boxes
function BlockQuote(el)
  if #el.content > 0 then
    local first = el.content[1]
    if first.t == "Para" and #first.content > 0 then
      local first_inline = first.content[1]

      -- Epigraph detection: blockquote starting with italic text in quotes
      if first_inline.t == "Emph" then
        local emph_text = pandoc.utils.stringify(first_inline)
        if emph_text:match('^[\"\x93]') or emph_text:match("^[\'\x91]") then
          -- Collect all quote text and look for attribution
          local quote_parts = {}
          local attribution = ""

          for _, block in ipairs(el.content) do
            if block.t == "Para" then
              local line = pandoc.utils.stringify(block)
              -- Check for attribution line: starts with -- or ---
              if line:match("^%-%-") then
                attribution = line:gsub("^%-+%s*", "")
              else
                table.insert(quote_parts, line)
              end
            end
          end

          local quote_text = table.concat(quote_parts, " ")
          -- Strip surrounding quote marks
          quote_text = quote_text:gsub('^[\"\x93\x94]', '')
          quote_text = quote_text:gsub('[\"\x93\x94]$', '')

          return pandoc.RawBlock("latex",
            "\\zkepigraph{" .. quote_text .. "}{" .. attribution .. "}")
        end
      end

      -- Auto-detect blockquotes starting with "Technical Detail"
      if first_inline.t == "Strong" then
        local text = pandoc.utils.stringify(first_inline)
        local env = nil
        local skip_label = false

        if text:match("^Technical Detail") then
          env = "technicalbox"
          skip_label = true
        end

        if env then
          local blocks = {}
          table.insert(blocks, pandoc.RawBlock("latex", "\\begin{" .. env .. "}"))
          -- Rebuild the first paragraph without the bold label
          if skip_label then
            local new_inlines = {}
            local started = false
            for i, inline in ipairs(first.content) do
              if i == 1 then
                -- skip the Strong element (the label)
              elseif not started and inline.t == "Space" then
                -- skip space after label
                started = true
              else
                started = true
                table.insert(new_inlines, inline)
              end
            end
            if #new_inlines > 0 then
              table.insert(blocks, pandoc.Para(new_inlines))
            end
          else
            table.insert(blocks, first)
          end
          -- Add remaining content
          for i = 2, #el.content do
            table.insert(blocks, el.content[i])
          end
          table.insert(blocks, pandoc.RawBlock("latex", "\\end{" .. env .. "}"))
          return blocks
        end
      end
    end
  end
end

-- ═══════════════════════════════════════════════════════════════════════════
--  BLOCKS FILTER: Process the full block list to suppress redundant HRs
--  and convert Part headings. This replaces the individual Header and
--  HorizontalRule functions with context-aware processing.
-- ═══════════════════════════════════════════════════════════════════════════

function Blocks(blocks)
  local result = {}
  local n = #blocks

  for i = 1, n do
    local el = blocks[i]

    -- Handle Part headings → \partdivider
    if el.t == "Header" and el.level == 1 then
      local text = pandoc.utils.stringify(el)
      if text:match("^Part [IVX]+:") or text:match("^Part [IVX]+ ") then
        table.insert(result, pandoc.RawBlock("latex",
          "\\partdivider{" .. text .. "}"))
        goto continue
      end
    end

    -- Handle HorizontalRule: suppress most, keep only structural ones
    if el.t == "HorizontalRule" then
      -- Look at neighbors to decide if this HR is redundant
      local prev = (i > 1) and blocks[i - 1] or nil
      local next_el = (i < n) and blocks[i + 1] or nil

      -- Suppress HR if next element is a Header (heading formatting suffices)
      if next_el and next_el.t == "Header" then
        goto continue
      end

      -- Suppress HR if previous element is a Header (heading formatting suffices)
      if prev and prev.t == "Header" then
        goto continue
      end

      -- Suppress HR if next element is a RawBlock we just created (partdivider)
      if next_el and next_el.t == "RawBlock" then
        goto continue
      end

      -- Suppress HR if previous element is a RawBlock (partdivider, epigraph)
      if prev and prev.t == "RawBlock" then
        local content = prev.text or ""
        if content:match("partdivider") or content:match("zkepigraph") then
          goto continue
        end
      end

      -- Suppress HR at the very start or end of the document
      if i <= 2 or i >= n - 1 then
        goto continue
      end

      -- Keep this HR — render as subtle vertical space only (no visible rule)
      -- On dark backgrounds, visible gradient rules between every section
      -- create visual noise. A clean vertical gap is sufficient.
      table.insert(result, pandoc.RawBlock("latex",
        "\\par\\vspace{18pt}"))
      goto continue
    end

    -- Pass everything else through unchanged
    table.insert(result, el)

    ::continue::
  end

  return result
end
