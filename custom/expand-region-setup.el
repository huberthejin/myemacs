(use-package expand-region
  :config
  (progn
    (global-set-key (kbd "C-=") 'er/expand-region)
    (global-set-key (kbd "C--") 'er/contract-region)
    )
  )

(provide 'expand-region-setup)
