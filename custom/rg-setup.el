
(use-package rg
  :config
  (progn
    (setq rg-keymap-prefix (kbd "C-c r"))
    (rg-enable-default-bindings)
    (setq rg-custom-type-aliases
  '(("cc" .    "*.[chH]  *.[chH].in  *.cats *.enum")
    ("ch" .    "*.[hH]  *.[hH].in  *.cats *.enum")))
    )
  )

(provide 'rg-setup)
