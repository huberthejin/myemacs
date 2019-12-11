
;;=========== C/C++ ==================

(require 'xcscope)
;; Always enbable cscope.
(cscope-setup)

(define-key global-map [(ctrl f3)] 'cscope-history-forward-line-current-result)
(define-key global-map [(ctrl f4)] 'cscope-history-backward-line-current-result)

;; start auto-complete with emacs
(use-package auto-complete
  :init
  (progn
    (require 'auto-complete-config)
    (ac-config-default)
    (global-auto-complete-mode t)
    )
  )

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



(use-package auto-complete-c-headers)

;; let's define a function which initializes auto-complete-c-headers and gets called for c/c++ hooks
(defun my:ac-c-header-init ()
;;    (require 'auto-complete-c-headers)
    (add-to-list 'ac-sources 'ac-source-c-headers)
    (add-to-list 'achead:include-directories '"/usr/include/c++/7")
    (add-to-list 'achead:include-directories '"/usr/include/x86_64-linux-gnu/c++/7")
    (add-to-list 'achead:include-directories '"/usr/include/c++/7/backward")
    (add-to-list 'achead:include-directories '"/usr/lib/gcc/x86_64-linux-gnu/7/include")
    (add-to-list 'achead:include-directories '"/usr/local/include")
    (add-to-list 'achead:include-directories '"/usr/lib/gcc/x86_64-linux-gnu/7/include-fixed")
    (add-to-list 'achead:include-directories '"/usr/include/x86_64-linux-gnu")
    (add-to-list 'achead:include-directories '"/usr/include")
    )

;; now let's call this function from c/c++ hooks
(add-hook 'c++-mode-hook 'my:ac-c-header-init)
(add-hook 'c-mode-hook 'my:ac-c-header-init)

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
;; let's define a function which adds semantic as a suggestion backend to auto complete
;; and hook this function to c-mode-common-hook
(defun my:add-semantic-to-autocomplete()
  (add-to-list 'ac-sources 'ac-source-semantic)
)
(add-hook 'c-mode-common-hook 'my:add-semantic-to-autocomplete)
;; turn on ede mode
(global-ede-mode 1)
;; create a project for our program.
;(ede-cpp-root-project "dcoBuild" :file "/home/hjin/work/dcoBuild/Makefile"
;		      :include-path '( "/include/" "/sdk-build/sdkcmn/code/include/app/") )

;; you can use system-include-path for setting up the system header file locations.
;; turn on automatic reparsing of open buffers in semantic
(global-semantic-idle-scheduler-mode 1)




(provide 'complete1-setup)
