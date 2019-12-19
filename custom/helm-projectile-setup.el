(use-package helm-projectile
  :init
  (helm-projectile-on)
  (setq projectile-completion-system 'helm)
  (setq projectile-indexing-method 'alien)
  )
;; Fix C-c p undefined issue.
(define-key projectile-mode-map (kbd "C-c p") 'projectile-command-map)


(provide 'helm-projectile-setup)
