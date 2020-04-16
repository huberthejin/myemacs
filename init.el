

;; 1 is vm laptop,
;; 2 is vnc office Monitor
;; 3 is vnc office.
;; 4 is vnc home DELL monitor
(setq laptop 4)

(defun adjustWindowSize (myWinWidth myWinHeight myFontSize)
  "My change window setting."
  (interactive)
  ;; initial window
  (add-to-list 'initial-frame-alist `(width . ,myWinWidth))
  (add-to-list 'initial-frame-alist `(height . ,myWinHeight))
  (add-to-list 'default-frame-alist `(width . ,myWinWidth))
  (add-to-list 'default-frame-alist `(height . ,myWinHeight))
  ;; Set font size to 100/10 = 10 pt.
  (set-face-attribute 'default nil :height myFontSize)
  )

(if ( = laptop 1)
    (adjustWindowSize 180 48 140)
  )

(if ( = laptop 2)
    (adjustWindowSize 280 80 90)
  )

(if ( = laptop 3)
    (adjustWindowSize 230 60 100)
    )

(if ( = laptop 4)
    (adjustWindowSize 230 80 100)
    )


;; =============pakcages =====================
(require 'package)
(setq package-check-signature nil)
(add-to-list 'package-archives '("melpa" . "https://melpa.org/packages/") t)
(package-initialize)

(when (not package-archive-contents)
    (package-refresh-contents))

(unless (package-installed-p 'use-package)
  (package-install 'use-package))

(add-to-list 'load-path "~/.emacs.d/custom")
(require 'use-package)
(setq use-package-always-ensure t)

;; ==============required packages ================
(require 'general-setup)

;; function-args
;; (require 'function-args)
;; (fa-config-default)
(custom-set-variables
 ;; custom-set-variables was added by Custom.
 ;; If you edit it by hand, you could mess it up, so be careful.
 ;; Your init file should contain only one such instance.
 ;; If there is more than one, they won't work right.
 '(package-selected-packages
   (quote
    (xcscope auto-complete-c-headers auto-complete-config auto-complete company-irony-c-headers irony-eldoc zygospore helm-gtags helm yasnippet ws-butler volatile-highlights use-package undo-tree iedit dtrt-indent counsel-projectile company clean-aindent-mode anzu company-irony flycheck-irony flycheck irony))))
(custom-set-faces
 ;; custom-set-faces was added by Custom.
 ;; If you edit it by hand, you could mess it up, so be careful.
 ;; Your init file should contain only one such instance.
 ;; If there is more than one, they won't work right.
 '(rainbow-delimiters-depth-1-face ((t (:foreground "dark orange"))))
 '(rainbow-delimiters-depth-2-face ((t (:foreground "deep sky blue"))))
 '(rainbow-delimiters-depth-3-face ((t (:foreground "chartreuse"))))
 '(rainbow-delimiters-depth-4-face ((t (:foreground "orchid"))))
 '(rainbow-delimiters-depth-5-face ((t (:foreground "yellow"))))
 '(rainbow-delimiters-depth-6-face ((t (:foreground "deep pink"))))
 '(rainbow-delimiters-depth-7-face ((t (:foreground "spring green"))))
 '(rainbow-delimiters-depth-8-face ((t (:foreground "sienna1")))))

;;============================
(setq launchdir default-directory)

