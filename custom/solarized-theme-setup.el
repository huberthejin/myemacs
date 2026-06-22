;; The themes are intended to be used with GUI

(use-package solarized-theme
  :config
  ;;(load-theme 'solarized-dark t)
  ;; (load-theme 'solarized-light t)
  ;; (load-theme 'solarized-selenized-light t)
  ;; (load-theme 'solarized-selenized-white t)
  ;; (load-theme 'solarized-light-high-contrast t)
  ;; (load-theme 'solarized-gruvbox-light t)
  )
(require 'solarized-selenized-light-hj-theme)
;; The custom theme file lives in ~/.emacs.d/custom, which is on `load-path'
;; but not on `custom-theme-load-path'; without this `load-theme' fails with
;; "Unable to find theme file".
(add-to-list 'custom-theme-load-path
             (expand-file-name "custom" user-emacs-directory))
(load-theme 'solarized-selenized-light-hj t)



(provide 'solarized-theme-setup)
