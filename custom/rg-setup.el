
(use-package rg
  :config
  (progn
    (setq rg-keymap-prefix (kbd "C-c r"))
    (rg-enable-default-bindings)
    (setq rg-custom-type-aliases
  '(("cc" .    "*.[chH]  *.[chH].in  *.cats *.enum *.enumh *.enumc")
    ("ch" .    "*.[hH]  *.[hH].in  *.cats *.enum *.enumh *.enumc")
    ("cmd" .    "*.cmd")
    ))
    )
  )

(provide 'rg-setup)
