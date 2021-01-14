
(use-package rg
  :config
  (progn
    (setq rg-keymap-prefix (kbd "C-c r"))
    (rg-enable-default-bindings)
    (setq rg-custom-type-aliases
  '(("cc" .    "*.[chH]  *.[chH].in *.in *.cc *.cats *.enum *.enumh *.enumc *.pl *.bag *.yang")
    ("ch" .    "*.[hH]  *.[hH].in  *.cats *.enum *.enumh *.enumc")
    ("cmd" .    "*.cmd")
    ))
    )
  )

(provide 'rg-setup)
