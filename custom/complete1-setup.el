
;;=========== C/C++ ==================

(require 'xcscope)
;; Always enbable cscope.
(cscope-setup)

(define-key global-map [(ctrl f3)] 'cscope-history-forward-line-current-result)
(define-key global-map [(ctrl f4)] 'cscope-history-backward-line-current-result)

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

;; We are going to use company instead
;;(require 'auto-complete-setup)


(provide 'complete1-setup)
