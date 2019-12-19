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
