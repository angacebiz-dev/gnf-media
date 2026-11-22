"""camera list for scene4. ground=True: z values are heights above the terrain at that x,y.
Story places: Goliath G=(5,12), David's run lane y~12 from x=-7 to 3, Israel line x~-9, camp x~-24, Saul's tent at x=300."""
G = dict(fstop=2.2, ground=True, sun_el=28, sun_az=-35)
BG = {
 "wide":      dict(cam=(0, -18, 11), tgt=(0, 22, 2), lens=22, fstop=None, ground=False, sun_el=28, sun_az=-35),
 "gol_low":   dict(G, cam=(3.4, 8.8, 0.35), tgt=(5.0, 12.5, 3.8), lens=18, fstop=2.0),
 "gol_med":   dict(G, cam=(4.0, 7.0, 1.7), tgt=(5.2, 13.0, 2.2), lens=30),
 "israel":    dict(G, cam=(-12.5, 5.5, 1.7), tgt=(0.0, 12.0, 1.2), lens=28, fstop=2.8),
 "camp":      dict(G, cam=(-19.0, 7.0, 1.6), tgt=(-24.0, 18.0, 2.0), lens=26, fstop=2.6),
 "tent_in":   dict(cam=(300.0, -3.6, 1.6), tgt=(300.0, 2.6, 1.6), lens=24, fstop=2.0, ground=False, sun_el=28, sun_az=-35),
 "tent_cu":   dict(cam=(300.6, -1.0, 1.5), tgt=(299.8, 2.6, 1.7), lens=40, fstop=1.6, ground=False, sun_el=28, sun_az=-35),
 "brook_cu":  dict(G, cam=(0.6, -2.0, 0.55), tgt=(1.0, 2.0, 0.05), lens=30, fstop=1.6),
 "david_med": dict(G, cam=(-3.6, 8.2, 1.4), tgt=(-6.0, 13.0, 1.6), lens=30, fstop=2.0),
 "ots":       dict(G, cam=(-7.5, 10.0, 1.1), tgt=(5.0, 13.0, 2.8), lens=26, fstop=4.0),
 "run_side":  dict(G, cam=(-1.0, 3.0, 1.3), tgt=(-1.0, 14.0, 1.3), lens=24, fstop=3.0),
 "sky_up":    dict(G, cam=(0.0, 8.0, 0.3), tgt=(1.5, 14.0, 6.5), lens=22, fstop=None),
 "fall":      dict(G, cam=(2.5, 7.5, 0.25), tgt=(5.0, 14.0, 0.7), lens=22, fstop=2.2),
 "victory":   dict(G, cam=(-1.0, 6.0, 0.45), tgt=(0.0, 12.0, 2.2), lens=22, fstop=2.5, sun_el=12, sun_az=-20),
 "end_cu":    dict(G, cam=(-2.0, 9.0, 1.4), tgt=(-3.0, 14.0, 1.6), lens=50, fstop=1.4, sun_el=12, sun_az=-20),
}
