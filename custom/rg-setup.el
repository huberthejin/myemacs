
(use-package rg
  :config
  (progn
    (setq rg-keymap-prefix (kbd "C-c r"))
    (rg-enable-default-bindings)
    )
  )

(provide 'rg-setup)
