
;;=========== C/C++ ==================



;;(require 'auto-complete)
;; do default config for auto-complete


;; start yasnippet with emacs
;;(add-to-list 'load-path "~/.emacs.d/elpa/yasnippet-20190724.1204")
;;(use-package yasnippet
;;  :init
;;  (progn
;;    (yas-global-mode 1)
;;    (define-key yas-minor-mode-map (kbd "TAB") nil)
;;    (define-key yas-minor-mode-map (kbd "<tab>") nil)
;;    (define-key yas-minor-mode-map (kbd "<C-tab>") #'yas-expand)
;;    )
;;  )




;; Fix iedit bug in Mac
;;(define-key global-map (kbd "C-c ;") 'iedit-mode)

;; start flymake-google-cpplint-load
;; let's define a function for flymake initialization
;;(defun my:flymake-google-init ()
;;  (require 'flymake-google-cpplint)
;;  (custom-set-variables
;;   '(flymake-google-cpplint-command "/opt/local/Library/Frameworks/Python.framework/Versions/2.7/bin/cpplint"))
;;  (flymake-google-cpplint-load)
;;)
;;(add-hook 'c-mode-hook 'my:flymake-google-init)
;;(add-hook 'c++-mode-hook 'my:flymake-google-init)

;; start google-c-style with emacs
;;(require 'google-c-style)
;;(add-hook 'c-mode-common-hook 'google-set-c-style)
;;(add-hook 'c-mode-common-hook 'google-make-newline-indent)

;; turn on Semantic
(semantic-mode 1)
;; turn on ede mode
(global-ede-mode 1)
;; create a project for our program.
;(ede-cpp-root-project "dcoBuild" :file "/home/hjin/work/dcoBuild/Makefile"
;		      :include-path '( "/include/" "/sdk-build/sdkcmn/code/include/app/") )

;; you can use system-include-path for setting up the system header file locations.
;; turn on automatic reparsing of open buffers in semantic
(global-semantic-idle-scheduler-mode 1)




(provide 'semantic-setup)
