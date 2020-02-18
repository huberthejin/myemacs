
;; Activate next-error-follow-minor-mode with C-c C-f. 
;; Use C-h m inside a results buffer to show all available keybindings.

(use-package ag
  :config
  (progn

    (global-set-key (kbd "C-c a a") 'ag)
    (global-set-key (kbd "C-c a d") 'ag-project-dired)
    (global-set-key (kbd "C-c a f") 'ag-project-files)
    (global-set-key (kbd "C-c a p") 'ag-project)
    (global-set-key (kbd "C-c a r") 'ag-project-regexp)

    (setq ag-highlight-search t)
    (setq ag-group-matches nil)

    )
  )



(provide 'ag-setup)
