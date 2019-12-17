
;; start auto-complete with emacs
(use-package auto-complete
  :init
  (progn
    (require 'auto-complete-config)
    (ac-config-default)
    (global-auto-complete-mode t)
    )
  )

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

;; let's define a function which adds semantic as a suggestion backend to auto complete
;; and hook this function to c-mode-common-hook
(defun my:add-semantic-to-autocomplete()
  (add-to-list 'ac-sources 'ac-source-semantic)
  )
(add-hook 'c-mode-common-hook 'my:add-semantic-to-autocomplete)



(provide 'auto-complete-setup)
