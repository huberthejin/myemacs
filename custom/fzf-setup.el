
;; Activate next-error-follow-minor-mode with C-c C-f.
;; Use C-h m inside a results buffer to show all available keybindings.

(use-package fzf
  :config
  (progn

    (global-set-key (kbd "C-c z z") 'fzf)
    (global-set-key (kbd "C-c z f") 'fzf-find-file)
    (global-set-key (kbd "C-c z d") 'fzf-directory)
    (global-set-key (kbd "C-c z g") 'fzf-git)
    (global-set-key (kbd "C-c a r") 'fzf-grep)
    )
  )

;; (setq fzf/directory-start default-directory)

(provide 'fzf-setup)
