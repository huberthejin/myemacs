;; setup GDB

(setq gdb-use-separate-io-buffer 1)


;; hook function loaded when starting gdb-many-windows, change the default layout of many-windows, this hook function can not be hooked in gdb-setup-windows, because assamble-buffer has not completed initialization yet, can not be set to window
(defadvice gdb-frame-handler (after activate)
  (if gdb-use-separate-io-buffer
      (advice_separate_io)
    (advice_no_separate_io)))

 ;; generate gdb layout without a separate IO window
(defun advice_no_separate_io()
 ;; The default function that generates gdb-assembler-buffer itself will also be designed to call gdb-frame-handler-1, adding this condition to avoid infinite recursive calls
  (if (not (gdb-get-buffer 'gdb-assembler-buffer))
      (progn
	(shrink-window-horizontally ( / (window-width) 3))

	(other-window 1)
	(split-window-horizontally)

	(other-window 1)
	(gdb-set-window-buffer (gdb-stack-buffer-name))

	(other-window 1)
	(split-window-horizontally)

	(other-window 1)
	(gdb-set-window-buffer (gdb-get-buffer-create 'gdb-assembler-buffer))
	(split-window-horizontally  (/ ( * (window-width) 2) 3))

	(other-window 1)
	(gdb-set-window-buffer (gdb-get-buffer-create 'gdb-registers-buffer))

	(other-window 1)
	(toggle-current-window-dedication)
	(gdb-set-window-buffer (get-buffer-create 'gdb-memory-buffer))
	(toggle-current-window-dedication)

	(other-window 2)
	)))

 ;; generate gdb layout with separate IO windows
(defun advice_separate_io()
 ;; The default function that generates gdb-assembler-buffer itself will also be designed to call gdb-frame-handler-1, adding this condition to avoid infinite recursive calls
  (if (not (gdb-get-buffer 'gdb-disassembly-buffer))
      (progn

    ;; gdb cmd line window
	(split-window-horizontally)
	(enlarge-window-horizontally ( / (window-width) 3))

    ;; input/out
	(other-window 1)
	 ;; can not be used here (gdb-set-window-buffer (gdb-get-buffer-create 'gdb-inferior-io)) instead,
	 ;; because when the state of gdb-use-separate-io-buffer is turned on, it will additionally call some functions to locate the input and output of gdb to the buffer.
	(gdb-set-window-buffer (gdb-inferior-io-name))

    ;; Locals/Registers window
	(other-window 1)
	(split-window-horizontally)

    ;; Stack frames window
	(other-window 1)
	(gdb-set-window-buffer (gdb-stack-buffer-name))

    ;; Source code windw, no change.
	(other-window 1)

    ;; disassembly window
	(other-window 1)
    (split-window-horizontally  (/ ( * (window-width) 2) 3))
    (set-window-dedicated-p (frame-selected-window) nil)
    (set-window-buffer (frame-selected-window) (gdb-get-buffer-create 'gdb-disassembly-buffer))
    (set-window-dedicated-p (frame-selected-window) 1)


    ;; registers window
	(other-window 1)
	(gdb-set-window-buffer (gdb-get-buffer-create 'gdb-registers-buffer))

    ;; memory buffer window
	(other-window 1)
    (set-window-dedicated-p (frame-selected-window) nil)
	(set-window-buffer (frame-selected-window) (gdb-get-buffer-create 'gdb-memory-buffer))
    (set-window-dedicated-p (frame-selected-window) 1)

    ;; Back to gdb cmd line window
	(other-window 2)
	))
  )


(provide 'gdb-setup)
