
(require 'xcscope)
;; Always enbable cscope.
(cscope-setup)

(define-key global-map [(ctrl f3)] 'cscope-history-forward-line-current-result)
(define-key global-map [(ctrl f4)] 'cscope-history-backward-line-current-result)

(provide 'xcscope-setup)
