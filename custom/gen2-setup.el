

;; ***************** define my own gen2 functions here **********************

;;This increase ibuffer MRL Name size to 50 bytes. 
(setq ibuffer-formats 
      '((mark modified read-only " "
              (name 50 50 :left :elide)
              " "
              (size 9 -1 :right)
              " "
              (mode 16 16 :left :elide)
              " " filename-and-process)
        (mark " "
              (name 16 -1)
              " " filename)))

(provide 'gen2-setup)
