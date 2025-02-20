return {

    "nvim-telescope/telescope-file-browser.nvim",
    -- local fb_actions = require "telescope".extensions.file_browser.actions
    -- fb_actions = require "telescope".extensions.file_browser.actions,
    -- local fb_actions = require "telescope".extensions.file_browser.actions,
   dependencies = { "nvim-telescope/telescope.nvim", "nvim-lua/plenary.nvim" },
   -- require("telescope").load_extension "file_browser",
   -- extensions = function(_, extensions)
   --    -- opts parameter is the default options table
   --    -- the function is lazy loaded so cmp is able to be required
   --    
   --    local fb_actions = require "telescope".extensions.file_browser.actions
   --    opts.extensions.file_browser.theme = "ivy"
   --    extensions.file_browser.mappings = {
   --        ["i"] = {
   --          -- your custom insert mode mappings
   --                -- ["<C-a>"] = goto_home_dir,
   --                -- ["<C-h>"] = function() requires("telescope").extensions.file_browser.actions.goto_home_dir end,
   --                -- ["<C-x>"] = function() goto_home_dir() end,
   --                ["<C-h>"] = fb_actions.goto_home_dir,
   --                ["<C-x>"] = function() requires("telescope") end,
   --        },
   --    }
   --
   -- end,
}
