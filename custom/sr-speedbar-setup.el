;; sr-speedbar-toggle

(use-package sr-speedbar
  :config
  (progn
    (setq speedbar-show-unknown-files t) ; show all files
    (setq speedbar-use-images nil) ; use text for buttons
    (setq sr-speedbar-right-side nil) ; put on left side
    )
  )



(provide 'sr-speedbar-setup)
