
;; turn on Semantic
;; Display current function on the first line.
;;(use-package stickyfunc-enhance)
;;(add-to-list 'semantic-default-submodes 'global-semantic-stickyfunc-mode)
(semantic-mode 1)
;;(require 'stickyfunc-enhance)


(setq semantic-default-submodes
      '(;; Perform semantic actions during idle time
        global-semantic-idle-scheduler-mode
        (semantic-idle-scheduler-idle-time 5)
        ;; Use a database of parsed tags
        global-semanticdb-minor-mode
        ;; Decorate buffers with additional semantic information
        global-semantic-decoration-mode
        ;; Highlight the name of the function you're currently in
        global-semantic-highlight-func-mode
        ;; show the name of the function at the top in a sticky
        global-semantic-stickyfunc-mode
        ;; code completions during idle time
        global-semantic-idle-completions-mode
        ;; Generate a summary of the current tag when idle
        global-semantic-idle-summary-mode
        ;; Show a breadcrumb of location during idle time
        global-semantic-idle-breadcrumbs-mode
        ;; Switch to recently changed tags with `semantic-mrub-switch-tags',
        ;; or `C-x B'
        global-semantic-mru-bookmark-mode))

;;;; change db directory
(setq semanticdb-default-save-directory "/nobackup/hubjin/semanticdb/" )
;;;; wait for 1 second before active scheduler
(setq semantic-idle-scheduler-idle-time 1 )
;;;; no verbose messages
(setq semantic-idle-scheduler-verbose-flag nil )
;;;; If non-nil, disable display of working messages while reparsing
(setq semantic-idle-scheduler-no-working-message nil)
;;;; If non-nil, show working messages in the mode line
(setq semantic-idle-scheduler-working-in-modeline-flag nil )

;;;; Wait for 20 seconds before doing idle parsing
(setq semantic-idle-scheduler-work-idle-time 5)
;;;; Parse the file in the same directory
(setq semantic-idle-work-parse-neighboring-files-flag 1 )

;;;; Display completions in a tooltip
(setq semantic-complete-inline-analyzer-idle-displayer-class  'semantic-displayer-tooltip)



(provide 'semantic-setup)
