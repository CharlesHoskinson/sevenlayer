-- kindle-filter.lua
-- Pandoc Lua filter for Kindle EPUB output
-- Adapts box-filter.lua for HTML/EPUB output instead of LaTeX
-- Handles: Part dividers, epigraphs, styled boxes, horizontal rules.

-- Map div classes to HTML div classes for CSS styling
local box_map = {
  technical  = "technical-box",
  insight    = "insight-box",
  caution    = "caution-box",
  example    = "example-box",
  patient    = "insight-box",
  regulatory = "example-box",
}

-- Handle fenced divs: ::: {.technical} ... :::
function Div(el)
  for cls, html_cls in pairs(box_map) do
    if el.classes:includes(cls) then
      local blocks = {}
      table.insert(blocks, pandoc.RawBlock("html",
        '<div class="' .. html_cls .. '">'))
      for _, b in ipairs(el.content) do
        table.insert(blocks, b)
      end
      table.insert(blocks, pandoc.RawBlock("html", '</div>'))
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
          local quote_parts = {}
          local attribution = ""

          for _, block in ipairs(el.content) do
            if block.t == "Para" then
              local line = pandoc.utils.stringify(block)
              if line:match("^%-%-") then
                attribution = line:gsub("^%-+%s*", "")
              else
                table.insert(quote_parts, line)
              end
            end
          end

          local quote_text = table.concat(quote_parts, " ")
          quote_text = quote_text:gsub('^[\"\x93\x94]', '')
          quote_text = quote_text:gsub('[\"\x93\x94]$', '')

          local html = '<div class="epigraph">\n'
          html = html .. '<p><em>' .. quote_text .. '</em></p>\n'
          if attribution ~= "" then
            html = html .. '<p class="attribution">' .. attribution .. '</p>\n'
          end
          html = html .. '</div>'

          return pandoc.RawBlock("html", html)
        end
      end

      -- Auto-detect blockquotes starting with "Technical Detail"
      if first_inline.t == "Strong" then
        local text = pandoc.utils.stringify(first_inline)
        if text:match("^Technical Detail") then
          local blocks = {}
          table.insert(blocks, pandoc.RawBlock("html",
            '<div class="technical-box">'))
          -- Rebuild without the bold label
          local new_inlines = {}
          local started = false
          for i, inline in ipairs(first.content) do
            if i == 1 then
              -- skip
            elseif not started and inline.t == "Space" then
              started = true
            else
              started = true
              table.insert(new_inlines, inline)
            end
          end
          if #new_inlines > 0 then
            table.insert(blocks, pandoc.Para(new_inlines))
          end
          for i = 2, #el.content do
            table.insert(blocks, el.content[i])
          end
          table.insert(blocks, pandoc.RawBlock("html", '</div>'))
          return blocks
        end
      end
    end
  end
end

-- Process blocks: Part headings, HR suppression
function Blocks(blocks)
  local result = {}
  local n = #blocks

  for i = 1, n do
    local el = blocks[i]

    -- Handle Part headings → styled div
    if el.t == "Header" and el.level == 1 then
      local text = pandoc.utils.stringify(el)
      if text:match("^Part [IVX]+:") or text:match("^Part [IVX]+ ") then
        table.insert(result, pandoc.RawBlock("html",
          '<div class="part-divider"><p>' .. text .. '</p></div>'))
        goto continue
      end
    end

    -- Handle HorizontalRule: suppress most, keep structural ones
    if el.t == "HorizontalRule" then
      local prev = (i > 1) and blocks[i - 1] or nil
      local next_el = (i < n) and blocks[i + 1] or nil

      if next_el and next_el.t == "Header" then
        goto continue
      end
      if prev and prev.t == "Header" then
        goto continue
      end
      if next_el and next_el.t == "RawBlock" then
        goto continue
      end
      if prev and prev.t == "RawBlock" then
        local content = prev.text or ""
        if content:match("part%-divider") or content:match("epigraph") then
          goto continue
        end
      end
      if i <= 2 or i >= n - 1 then
        goto continue
      end

      -- Keep as simple HR
      table.insert(result, pandoc.RawBlock("html", "<hr />"))
      goto continue
    end

    table.insert(result, el)
    ::continue::
  end

  return result
end
