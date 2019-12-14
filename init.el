;; ====== EMACS windows (color, size) setting ========
(load-file "~/.emacs.d/custom/abyss-theme-source-code.el")

;; 1 is vm laptop,
;; 2 is vm office
(setq laptop 2)

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
    (adjustWindowSize 180 50 140)
  )

(if ( = laptop 2)
    (adjustWindowSize 230 60 110)
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
(require 'gdb-setup)
(require 'helm-setup)
(require 'helm-gtags-setup)
;; (require 'ggtags-setup)
(require 'c-setup)
(require 'cedet-setup)
(require 'editing-setup)
(require 'multiple-cursors-setup)
(require 'move-text-setup)

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
    (auto-complete-c-headers auto-complete-config auto-complete company-irony-c-headers irony-eldoc zygospore helm-gtags helm yasnippet ws-butler volatile-highlights use-package undo-tree iedit dtrt-indent counsel-projectile company clean-aindent-mode anzu company-irony flycheck-irony flycheck irony))))
(custom-set-faces
 ;; custom-set-faces was added by Custom.
 ;; If you edit it by hand, you could mess it up, so be careful.
 ;; Your init file should contain only one such instance.
 ;; If there is more than one, they won't work right.
 )

;;============================
(setq launchdir default-directory)

;; ==========complete ways ======
;; 1. completion old way
;;(require 'auto-complete-setup)
(require 'semantic-setup)

;; 2. complete with irony
;;(require 'completeirony-setup)
