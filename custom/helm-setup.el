(use-package helm
  :init
  (progn
    (require 'helm-config)
    ;; To fix error at compile:
    ;; Error (bytecomp): Forgot to expand macro with-helm-buffer in
    ;; (with-helm-buffer helm-echo-input-in-header-line)
    (if (version< "26.0.50" emacs-version)
        (eval-when-compile (require 'helm-lib)))

    ;; The default "C-x c" is quite close to "C-x C-c", which quits Emacs.
    ;; Changed to "C-c h". Note: We must set "C-c h" globally, because we
    ;; cannot change `helm-command-prefix-key' once `helm-config' is loaded.
    (global-set-key (kbd "C-c h") 'helm-command-prefix)
    (global-unset-key (kbd "C-x c"))

    (global-set-key (kbd "M-x") 'helm-M-x)
    (global-set-key (kbd "C-x C-f") 'helm-find-files)
    (global-set-key (kbd "C-x f") 'helm-for-files)
    (global-set-key (kbd "C-x r") 'helm-recentf)
    (global-set-key (kbd "M-y") 'helm-show-kill-ring)

    (define-key 'help-command (kbd "C-f") 'helm-apropos)
    (define-key 'help-command (kbd "r") 'helm-info-emacs)



    ;;(define-key helm-map (kbd "<tab>") 'helm-execute-persistent-action) ; rebihnd tab to do persistent action
    ;;(define-key helm-map (kbd "C-i") 'helm-execute-persistent-action) ; make TAB works in terminal
    ;;(define-key helm-map (kbd "C-z")  'helm-select-action) ; list actions using C-z


    ;;(add-to-list 'helm-sources-using-default-as-input 'helm-source-man-pages)

    ;;(global-set-key (kbd "C-x b") 'helm-buffers-list)
    ;; (global-set-key (kbd "C-h SPC") 'helm-all-mark-rings)
    ;;(global-set-key (kbd "C-c h o") 'helm-occur) ;; use helm-swoop now.


    ;;(define-key 'help-command (kbd "C-l") 'helm-locate-library)

    ;;; Save current position to mark ring
    (add-hook 'helm-goto-line-before-hook 'helm-save-current-pos-to-mark-ring)

    ;; show minibuffer history with Helm
    (define-key minibuffer-local-map (kbd "M-p") 'helm-minibuffer-history)
    (define-key minibuffer-local-map (kbd "M-n") 'helm-minibuffer-history)

    (define-key global-map [remap find-tag] 'helm-etags-select)

    (define-key global-map [remap list-buffers] 'helm-buffers-list)


    (helm-mode 1)
    )
  )

(require 'helm-swoop-setup)
(require 'helm-projectile-setup)



(provide 'helm-setup)
