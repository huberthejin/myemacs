;;; solarized-selenized-light-hj-theme.el --- Solarized Theme  -*- lexical-binding: t -*-



(require 'solarized)
;;(eval-when-compile
;;  (require 'solarized-palettes))

;; base0 is the default text font.

(defvar solarized-selenized-light-hj-color-palette-alist
  '( ;; selenized-light palette
    (base03      . "#fbf3db")
    (base02      . "#ece3cc")
    (base01      . "#909995")
    (base00      . "#fbf3db")
    (base0       . "#23373d")
    (base1       . "#3a4d53")
    (base2       . "#adbcbc")
    (base3       . "#cad8d9")
    (yellow      . "#ad8900")
    (orange      . "#c25d1e")
    (red         . "#d2212d")
    (magenta     . "#ca4898")
    (violet      . "#8762c6")
    (blue        . "#0072d4")
    (cyan        . "#009c8f")
    (green       . "#489100")
    (yellow-1bg  . "#f4e5c0")
    (yellow-1fg  . "#90792f")
    (yellow-2bg  . "#edd397")
    (yellow-2fg  . "#887640")
    (yellow-d    . "#b08b24")
    (yellow-l    . "#cea847")
    (orange-1bg  . "#f9dfc0")
    (orange-1fg  . "#a05c34")
    (orange-2bg  . "#f7c198")
    (orange-2fg  . "#956143")
    (orange-d    . "#c65e21")
    (orange-l    . "#e67b41")
    (red-1bg     . "#fedac1")
    (red-1fg     . "#ac403b")
    (red-2bg     . "#ffb39b")
    (red-2fg     . "#a04e48")
    (red-d       . "#d53926")
    (red-l       . "#f65a45")
    (magenta-1bg . "#f9ddd4")
    (magenta-1fg . "#a35285")
    (magenta-2bg . "#f7bdcb")
    (magenta-2fg . "#955b82")
    (magenta-d   . "#cd488f")
    (magenta-l   . "#ea68b0")
    (violet-1bg  . "#eedfdb")
    (violet-1fg  . "#735fa5")
    (violet-2bg  . "#dbc2df")
    (violet-2fg  . "#6f649b")
    (violet-d    . "#8355c0")
    (violet-l    . "#9c72e4")
    (blue-1bg    . "#e4e1de")
    (blue-1fg    . "#3369ae")
    (blue-2bg    . "#c0c7e5")
    (blue-2fg    . "#426ba2")
    (blue-d      . "#4872cb")
    (blue-l      . "#608eef")
    (cyan-1bg    . "#e1e9d2")
    (cyan-1fg    . "#2d867f")
    (cyan-2bg    . "#b9dcc8")
    (cyan-2fg    . "#3b817d")
    (cyan-d      . "#3ea08e")
    (cyan-l      . "#55beaf")
    (green-1bg   . "#e4e7bf")
    (green-1fg   . "#4b7f2e")
    (green-2bg   . "#c1d795")
    (green-2fg   . "#527c3f")
    (green-d     . "#569623")
    (green-l     . "#70b447")
    ;; palette end
    )
  "The solarized color palette alist")


(deftheme solarized-selenized-light-hj
  "The light variant of the Solarized colour theme with selenized color palette")

(solarized-with-color-variables 'dark 'solarized-selenized-light-hj
  solarized-selenized-light-hj-color-palette-alist)

(provide-theme 'solarized-selenized-light-hj)

(provide 'solarized-selenized-light-hj-theme)

;; Local Variables:
;; indent-tabs-mode: nil
;; End:

;;; solarized-selenized-light-hj-theme.el ends here

