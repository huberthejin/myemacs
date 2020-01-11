;; type / <word> RET to narrow the files. Can narrow repeatedly
;; type 9 to revert back to the full directory listing.

(use-package dired-narrow
  :ensure t
  :bind (:map dired-mode-map
              ("/" . dired-narrow)))

(provide 'dired-narrow-setup)
