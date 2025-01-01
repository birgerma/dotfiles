
# Custom commands in sudo mode:
alias 'sudo'='sudo '

# Navigation
alias ..='cd ..'

# Arch
alias pacman='sudo pacman'
## Fuzzy pacman/yay search
alias fpac='\pacman -Slq | fzf --multi --preview "\pacman -Si {1}" | xargs -ro sudo \pacman -S'
alias fyay='\yay -Slq | fzf --multi --preview "\yay -Si {1}" | xargs -ro \yay -S'

# Confirm rm
# alias rm='rm -i'
alias rm='rm -i --preserve-root'
alias mv='mv -i'
alias cp='cp -i'
alias ln='ln -i'

# Open files with default program
alias 'open'='gio open'

# Kanshi
alias "kanshi-restart"="systemctl --user restart kanshi"
alias "kanshi-status"="systemctl --user status kanshi"

# Tmux/tmuxinator
alias mux='tmuxinator'
alias muxor='tmuxinator '
# TMUX_DEFAULT_SESSION='base'
# alias tms="$HOME/.local/bin/tmux-fzf-session-choser.sh"
# alias tm='tmux a -t base || tmux new-session -s base'
 
# ls
alias ls='eza --icons'
# alias ls='ls --color=auto'
alias la='ls -la'
alias ll='eza --long --header --git --icons'
# PS1='[\u@\h \W]\$ '
# PS1='[@\h \W]\$ '
alias mkdir='mkdir -pv'
alias cat=bat
#alias path='echo -e ${PATH//:/\\n}'

alias now='date +"%T"'
alias nowdate='date +"%d-%m-%Y"'

# Emacs
alias 'em'='emacsclient -create-frame --alternate-editor="" -nw'
# alias 'em'='emacs -nw --with-profile custom'
#alias 'emacs'='emacsclient -create-frame --alternate-editor=""'

# Git aliases
alias 'gs'='git status'
alias 'git-remember'='git config credential.helper "cache --timeout=28800"'

# Make commands
# Auto run make on tex files
alias texmake='find . -type f -name "*.tex" -or -name "*.bib"|entr -r make'

