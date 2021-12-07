;; Run the follwing comamnd for profiling
;; ~/usr/bin/emacs -Q -l  ~/.emacs.d/profile-dotemacs.el -f profile-dotemacs

(setq gc-cons-threshold 40000000)

;; 1 is vm laptop,
;; 2 is vnc office Monitor
;; 3 is vnc office.
;; 4 is vnc home DELL monitor
(setq laptop 2)

(defun adjustWindowSize (myWinWidth myWinHeight myFontSize)
  "My change window setting."
  (interactive)
  ;; initial window
  (add-to-list 'initial-frame-alist `(width . ,myWinWidth))
  (add-to-list 'initial-frame-alist `(height . ,myWinHeight))
  (add-to-list 'default-frame-alist `(width . ,myWinWidth))
  (add-to-list 'default-frame-alist `(height . ,myWinHeight))

  ;; Fix the black cursor issue for emacsclient
  (add-to-list 'default-frame-alist `(cursor-color . "white"))

  ;; Set font size to 100/10 = 10 pt.
  (set-face-attribute 'default nil :height myFontSize)
  )

(if ( = laptop 1)
    (adjustWindowSize 180 48 140)
  )

(if ( = laptop 2)
    (adjustWindowSize 240 55 95)
  )

(if ( = laptop 3)
    (adjustWindowSize 230 60 100)
    )

(if ( = laptop 4)
    (adjustWindowSize 280 80 110)
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

;; ========= require/install all packages ==========
;; =================================================
;; (require 'general-setup)

;; ====== EMACS windows (color, size) setting ========
(require 'gruvbox-themes-setup)
;;(require 'kaolin-themes-setup)
;;(require 'moe-theme-setup)
;;(load-file "~/.emacs.d/custom/abyss-theme-source-code.el")
;;(require 'alect-themes-setup)
;;(require 'faff-theme-setup)
;;(setq frame-background-mode 'light)


;;(menu-bar-mode -1)
(tool-bar-mode -1)

;;size of garbage collector.
(setq gc-cons-threshold 100000000)

;; disable splash screen and startup messages.
(setq inhibit-splash-screen t)
(setq inhibit-startup-message t)

;; y or n is enough
(defalias 'yes-or-no-p 'y-or-n-p)

;; turn off sound
(setq visible-bell t)
(setq ring-bell-function 'ignore)

;; show unncessary whitespace that can mess up your diff
(add-hook 'prog-mode-hook
          (lambda () (interactive)
            (setq show-trailing-whitespace 1)))

;; use space to indent by default
(setq-default indent-tabs-mode nil)

;; set appearance of a tab that is represented by 4 spaces
(setq-default tab-width 4)

;; Open buffer in current window, not the other window(by default).
;(global-set-key "\C-x\C-b" 'buffer-menu)
(global-set-key "\C-x\C-b" 'ibuffer)

;; Now hashfiles
(setq create-lockfiles nil)

;; No backup files
(setq make-backup-files nil)

;; No auto-save files
(setq auto-save-default nil)

;; Reuse "C-x f" for finding a file
(global-unset-key (kbd "C-x f"))

;; Display line number on side
;;(global-linum-mode t)

;; Auto-refresh all buffers when files have changes on disk.
(global-auto-revert-mode t)

;; Load large TAGS file
(setq large-file-warning-threshold nil)

;; after copy Ctrl+c in Linux X11, you can paste by `yank' in emacssgdefggtrfdesffsfdf
(setq x-select-enable-clipboard t)

;; after mouse selection in X11, you can paste by `yank' in emacs
(setq x-select-enable-primary t)

;; show matching parenthesis
(show-paren-mode 1)

;; cursor jitter issue.
(setq auto-window-vscroll nil)

;; join lines
(global-set-key (kbd "M-j") (lambda ()(interactive)(join-line -1)) )

;; Always follow the symlink
(setq vc-follow-symlinks t)

;; Replace the active region just by typing text, and delete the
;; selected text just by hitting the Backspace key.
(delete-selection-mode 1)

(put 'narrow-to-region 'disabled nil)

(setq c-default-style "linux"
      c-basic-offset 4)

;; line-number will make emcas running slow.
(global-display-line-numbers-mode)

;; Diplay the full path file name
(setq frame-title-format
      (list '(buffer-file-name "%f" (dired-directory dired-directory "%b"))))

;; Disable suspend Button
(global-unset-key [(control z)])


;;;; ============= Individual setting above this line ===========
;; use dired-jump   C-x C-j
(require 'dired-x)

;;(require 'org-setup)
(require 'dired-narrow-setup)

;; C-x  then wait couple of seconds.
(require 'which-key-setup)
(require 'helm-setup)
(require 'helm-gtags-setup)

(require 'uniquify-setup)
;;(require 'yasnippet-setup)
(require 'smartparens-setup)
(require 'avy-setup)
(require 'expand-region-setup)
;;(require 'protobuf-setup)
;;(require 'cmake-setup)
(require 'column-indicator-setup)

;;(require 'magit-setup)
(unless (package-installed-p 'magit)
    (package-install 'magit))
(autoload 'magit-status "magit" nil t)

(require 'company-setup)
;;(require 'projectile-setup)
;;(require 'zygospore-setup)
;;(require 'gdb-setup)
;; (require 'ggtags-setup)
(require 'c-setup)
(require 'cedet-setup)
;;(require 'editing-setup)
(require 'multiple-cursors-setup)
(require 'move-text-setup)

(require 'ag-setup)
;;(require 'wgrep-setup)
;;(require 'wgrep-ag-setup)

(require 'ivy-counsel-setup)

;;(require 'rainbow-delimiters-setup)

(require 'fzf-setup)

;; ==========complete ways ======
;; 1. completion old way
(require 'xcscope-setup)
;;(require 'auto-complete-setup)
(require 'semantic-setup)

;; 2. complete with irony
;;(require 'completeirony-setup)



;;(require 'flycheck-setup)

;; ============ editing related =========

(require 'volatile-highlights-setup)
(require 'undo-tree-setup)
;;(require 'evil-setup)
(require 'clean-aindent-mode-setup)
;;(require 'dtrt-indent-setup)
(require 'ws-butler-setup)
(require 'comment-dwin-2-setup)
(require 'anzu-setup)
(require 'iedit-setup)
(require 'dumb-jump-setup)
(require 'rg-setup)
;;(require 'sr-speedbar-setup)

;; tabbar
;;(use-package tabbar
;;  :config (tabbar-mode 1) )

;; use Shirf and arrow key to move between windows
(windmove-default-keybindings)

;; Compilation
(global-set-key (kbd "<f8>") (lambda ()
                               (interactive)
                               (setq-local compilation-read-command nil)
                               (call-interactively 'compile)))

(setq
 ;; use gdb-many-windows by default
 gdb-many-windows t
 ;; Non-nil means display source file containing the main routine at startup
 gdb-show-main t
 )

;; automatically indent when press RET

;; activate whitespace-mode to view all whitespace characters
(global-set-key (kbd "C-c w") 'whitespace-mode)
(windmove-default-keybindings)

;; ========= Finish installing all packages ==========
;; ========= add my own functions here ===============
 (require 'general-setup)

;;============== end of general-setup =============
;; function-args
;; (require 'function-args)
;; (fa-config-default)
(custom-set-variables
 ;; custom-set-variables was added by Custom.
 ;; If you edit it by hand, you could mess it up, so be careful.
 ;; Your init file should contain only one such instance.
 ;; If there is more than one, they won't work right.
 '(package-selected-packages
   '(moe-theme xcscope auto-complete-c-headers auto-complete-config auto-complete company-irony-c-headers irony-eldoc zygospore helm-gtags helm yasnippet ws-butler volatile-highlights use-package undo-tree iedit dtrt-indent counsel-projectile company clean-aindent-mode anzu company-irony flycheck-irony flycheck irony))
 '(safe-local-variable-values '((eval when (fboundp 'rainbow-mode) (rainbow-mode 1)))))

;;============================
(setq launchdir default-directory)

(custom-set-faces
 ;; custom-set-faces was added by Custom.
 ;; If you edit it by hand, you could mess it up, so be careful.
 ;; Your init file should contain only one such instance.
 ;; If there is more than one, they won't work right.
 )
