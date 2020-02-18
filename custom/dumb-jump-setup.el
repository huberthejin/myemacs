
(use-package dumb-jump
  :config
  (progn
    (setq dumb-jump-selector 'helm)
    (setq dumb-jump-force-searcher 'ag)
    (setq dumb-jump-prefer-searcher 'ag)
    (setq dumb-jump-aggressive nil)
    )
  )


(provide 'dumb-jump-setup)
