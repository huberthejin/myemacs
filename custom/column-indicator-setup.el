(use-package fill-column-indicator
  :config
  (progn
    (setq fci-rule-column 80)
    )
  )

(setq fci-rule-width 1)
(setq fci-rule-color "darkblue")
;;(add-hook 'c-mode-hook 'fci-mode)


(provide 'column-indicator-setup)
