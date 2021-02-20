import pcbnew
import math

def p(px, py):
    return pcbnew.wxPoint(px * 1000000, py * 1000000)

def mp(p, mx, my):
    return pcbnew.wxPoint(p.x + mx * 1000000, p.y + my * 1000000)

def d(p1, p2):
    return math.sqrt((p2.x - p1.x)**2 + (p2.y - p1.y)**2) / 1000000

def mid_p(p1, p2):
    return pcbnew.wxPoint((p1.x + p2.x) / 2, (p1.y + p2.y) / 2)

def curve(p1, p2, p3, r):
    if r < 0.5:
        return [p2]

    r12 = min(d(p1, p2)/2, r/2)
    p12 = p2 - p(
        r12 * math.cos(math.atan2(p2.y - p1.y, p2.x - p1.x)),
        r12 * math.sin(math.atan2(p2.y - p1.y, p2.x - p1.x)))

    r23 = min(d(p2, p3)/2, r/2)
    p23 = p2 - p(
        r23 * math.cos(math.atan2(p2.y - p3.y, p2.x - p3.x)),
        r23 * math.sin(math.atan2(p2.y - p3.y, p2.x - p3.x)))

    p123 = mid_p(p12, p23)

    return curve(p1, p12, p123, r12) + curve(p123, p23, p3, r23)

def draw_segment(p1, p2, layer, width):
    pcb = pcbnew.GetBoard()
    ds = pcbnew.DRAWSEGMENT(pcb)
    pcb.Add(ds)
    ds.SetStart(p1)
    ds.SetEnd(p2)
    ds.SetLayer(layer)
    ds.SetWidth(max(1, int(width)))
    return ds

def draw_coords(coords, offset, layer, width):
    for i in range(len(coords)):
        start = coords[i - 1] if i > -1 else coords[len(coords) - 1]
        end = coords[i]
        draw_segment(start + offset, end + offset, layer, width)

def draw_edge_cuts(points, offset):
    coords = []

    for i in range(len(points)):
        r = points[i]["r"]
        a = points[i - 1]["p"] if i > -1 else points[len(points) - 1]["p"]
        b = points[i]["p"]
        c = points[i + 1]["p"] if i + 1 < len(points) else points[0]["p"]

        # text(b + offset, "+")
        coords += curve(a, b, c, r)
        # coords += [b]

    draw_coords(coords, offset, pcbnew.Edge_Cuts, 10000)

def show_drawings():
    pcb = pcbnew.GetBoard()
    for d in pcb.DrawingsList():
        print(type(d))
        print(d.GetLayerName())
        print(d.GetPosition())

def track(p1, p2, layer, width):
    pcb = pcbnew.GetBoard()
    t = pcbnew.TRACK(pcb)
    pcb.Add(t)
    t.SetStart(p1)
    t.SetEnd(p2)
    t.SetLayer(layer)
    t.SetWidth(width)
    return t

def track_coords(coords, offset, layer, width):
    for i in range(len(coords)-1):
        start = coords[i]
        end = coords[i+1]
        track(start + offset, end + offset, layer, width)

def draw_tracks(points, offset, layer):
    coords = []

    for i in range(len(points)):
        r = points[i]["r"]
        a = points[i - 1]["p"] if i > -1 else points[len(points) - 1]["p"]
        b = points[i]["p"]
        c = points[i + 1]["p"] if i + 1 < len(points) else points[0]["p"]

        # text(b + offset, "+")
        coords += curve(a, b, c, r)
        # coords += [b]

    track_coords(coords, offset, layer, 250000)

def text(p, text):
    pcb = pcbnew.GetBoard()
    t = pcbnew.TEXTE_PCB(pcb)
    pcb.Add(t)
    t.SetPosition(p)
    t.SetText(text)
    return t

def draw_corne_edge_cuts():
    # # top-plate
    # # left
    # draw_edge_cuts([
    #     {"p": p(0.000,   7.125), "r": 1.0},
    #     {"p": p(0.000,   63.125), "r": 1.0},
    #     {"p": p(55.630,  63.125), "r": 1.0},
    #     {"p": p(66.594,  77.940), "r": 1.0},
    #     {"p": p(103.960, 82.840), "r": 1.0},
    #     {"p": p(119.750, 92.00), "r": 1.0},
    #     {"p": p(133.500, 68.040), "r": 1.0},
    #     {"p": p(113.000, 56.250), "r": 1.0},
    #     {"p": p(113.000, 7.125), "r": 1.0},
    #     {"p": p(113.000, 4.750), "r": 1.0},
    #     {"p": p(94.000,  4.750), "r": 1.0},
    #     {"p": p(94.000,  2.375), "r": 1.0},
    #     {"p": p(75.000,  2.375), "r": 1.0},
    #     {"p": p(75.000,  0.000), "r": 1.0},
    #     {"p": p(57.000,  0.000), "r": 1.0},
    #     {"p": p(57.000,  2.375), "r": 1.0},
    #     {"p": p(38.000,  2.375), "r": 1.0},
    #     {"p": p(38.000,  7.125), "r": 1.0},
    # ], p(0, 0))
    # # right
    # draw_edge_cuts([
    #     {"p": p(274.500, 7.125), "r": 1.0},
    #     {"p": p(274.500, 63.125), "r": 1.0},
    #     {"p": p(218.870, 63.125), "r": 1.0},
    #     {"p": p(207.906, 77.940), "r": 1.0},
    #     {"p": p(170.540, 82.840), "r": 1.0},
    #     {"p": p(154.750, 92.00), "r": 1.0},
    #     {"p": p(141.000, 68.040), "r": 1.0},
    #     {"p": p(161.500, 56.250), "r": 1.0},
    #     {"p": p(161.500, 7.125), "r": 1.0},
    #     {"p": p(161.500, 4.750), "r": 1.0},
    #     {"p": p(180.500, 4.750), "r": 1.0},
    #     {"p": p(180.500, 2.375), "r": 1.0},
    #     {"p": p(199.500, 2.375), "r": 1.0},
    #     {"p": p(199.500, 0.000), "r": 1.0},
    #     {"p": p(217.500, 0.000), "r": 1.0},
    #     {"p": p(217.500, 2.375), "r": 1.0},
    #     {"p": p(236.500, 2.375), "r": 1.0},
    #     {"p": p(236.500, 7.125), "r": 1.0},
    # ], p(0, 0))

    # outline
    draw_edge_cuts([
        # Frame begin
        {"p": p(6.625, 7.125), "r": 0.0},
        {"p": p(6.625, -2.000), "r": 1.0},
        {"p": p(0.000, -2.000), "r": 1.0},
        {"p": p(0.000, -8.000), "r": 1.0},
        {"p": p(274.500, -8.000), "r": 1.0},
        {"p": p(274.500, -2.000), "r": 1.0},
        {"p": p(267.875, -2.000), "r": 1.0},
        {"p": p(267.875, 7.125), "r": 0.0},
        # Frame end
        # Body begin
        {"p": p(274.500, 7.125), "r": 1.0},
        {"p": p(274.500, 63.125), "r": 1.0},
        # Body end
        # Frame begin
        {"p": p(267.875, 63.125), "r": 0.0},
        {"p": p(267.875, 72.125), "r": 1.0},
        {"p": p(274.500, 72.125), "r": 1.0},
        {"p": p(274.500, 100.000), "r": 1.0},
        {"p": p(0.000, 100.000), "r": 1.0},
        {"p": p(0.000, 72.125), "r": 1.0},
        {"p": p(6.625, 72.125), "r": 1.0},
        {"p": p(6.625, 63.125), "r": 0.0},
        # Frame end
        # Body begin
        {"p": p(0.000, 63.125), "r": 1.0},
        {"p": p(0.000, 7.125), "r": 1.0},
        # Body end
    ], p(0, 0))
    # left top line
    draw_edge_cuts([
        # Frame begin
        {"p": p(11.375, 7.125), "r": 0.0},
        {"p": p(11.375, -2.000), "r": 1.0},
        {"p": p(121.33, -2.000), "r": 1.0},
        {"p": p(121.33, 7.125), "r": 0.0},
        # Frame end
        # Body begin
        {"p": p(113.000, 7.125), "r": 1.0},
        {"p": p(113.000, 4.750), "r": 1.0},
        {"p": p(94.000, 4.750), "r": 1.0},
        {"p": p(94.000, 2.375), "r": 1.0},
        {"p": p(75.000, 2.375), "r": 1.0},
        {"p": p(75.000, 0.000), "r": 1.0},
        {"p": p(57.000, 0.000), "r": 1.0},
        {"p": p(57.000, 2.375), "r": 1.0},
        {"p": p(38.000, 2.375), "r": 1.0},
        {"p": p(38.000, 7.125), "r": 1.0},
        # Body end
    ], p(0, 0))
    # right top line
    draw_edge_cuts([
        # Frame begin
        {"p": p(153.17, 7.125), "r": 0.0},
        {"p": p(153.17, -2.000), "r": 1.0},
        {"p": p(263.125, -2.000), "r": 1.0},
        {"p": p(263.125, 7.125), "r": 0.0},
        # Frame end
        # Body begin
        {"p": p(236.500, 7.125), "r": 1.0},
        {"p": p(236.500, 2.375), "r": 1.0},
        {"p": p(217.500, 2.375), "r": 1.0},
        {"p": p(217.500, 0.000), "r": 1.0},
        {"p": p(199.500, 0.000), "r": 1.0},
        {"p": p(199.500, 2.375), "r": 1.0},
        {"p": p(180.500, 2.375), "r": 1.0},
        {"p": p(180.500, 4.750), "r": 1.0},
        {"p": p(161.500, 4.750), "r": 1.0},
        {"p": p(161.500, 7.125), "r": 1.0},
        # Body end
    ], p(0, 0))
    # left bottom line
    draw_edge_cuts([
        # Frame begin
        {"p": p(11.375, 63.125), "r": 0.0},
        {"p": p(11.375, 72.125), "r": 1.0},
        {"p": p(44.625, 72.125), "r": 1.0},
        {"p": p(44.625, 63.125), "r": 0.0},
        # Frame end
    ], p(0, 0))
    # right bottom line
    draw_edge_cuts([
        # Frame begin
        {"p": p(229.875, 63.125), "r": 0.0},
        {"p": p(229.875, 72.125), "r": 1.0},
        {"p": p(263.125, 72.125), "r": 1.0},
        {"p": p(263.125, 63.125), "r": 0.0},
        # Frame end
    ], p(0, 0))
    # center
    draw_edge_cuts([
        # Frame begin
        {"p": p(126.08, 7.125), "r": 0.0},
        {"p": p(126.08, -2.000), "r": 1.0},
        {"p": p(148.42, -2.000), "r": 1.0},
        {"p": p(148.42, 7.125), "r": 0.0},
        # Frame end
        # Body begin
        {"p": p(141.000, 7.125), "r": 1.0},
        {"p": p(141.000, 68.040), "r": 1.0},
        {"p": p(154.750, 92.00), "r": 1.0},
        {"p": p(170.540, 82.840), "r": 1.0},
        {"p": p(207.906, 77.940), "r": 1.0},
        {"p": p(218.870, 63.125), "r": 1.0},
        # Body end
        # Frame begin
        {"p": p(225.125, 63.125), "r": 0.0},
        {"p": p(225.125, 72.125), "r": 1.0},
        {"p": p(218.500, 72.125), "r": 1.0},
        {"p": p(218.500, 94.00), "r": 1.0},
        {"p": p(56.000, 94.000), "r": 1.0},
        {"p": p(56.000, 72.125), "r": 1.0},
        {"p": p(49.375, 72.125), "r": 1.0},
        {"p": p(49.375, 63.125), "r": 0.0},
        # Frame end
        # Body begin
        {"p": p(55.630, 63.125), "r": 1.0},
        {"p": p(66.594, 77.940), "r": 1.0},
        {"p": p(103.960, 82.840), "r": 1.0},
        {"p": p(119.750, 92.000), "r": 1.0},
        {"p": p(133.500, 68.040), "r": 1.0},
        {"p": p(133.500, 7.125), "r": 1.0},
        # Body end
    ], p(0, 0))
    pcbnew.Refresh()

def set_corne_footprints():
    pcb = pcbnew.GetBoard()
    for ref, m in {
        # left
        "U1":    {"p": p(123.705, 26.765), "degree": 0,   "flip": False},  # Pro Micro
        "J1":    {"p": p(133.030, 54.635), "degree": 270, "flip": False},  # TRRS Jack
        "J2":    {"p": p(119.840, 47.375), "degree": 0,   "flip": False},  # OLED Jack
        "SH1":   {"p": p(18.500,  25.625), "degree": 0,   "flip": False},  # M2 Spacer Hole
        "SH2":   {"p": p(18.500,  44.625), "degree": 0,   "flip": False},  # M2 Spacer Hole
        "SH3":   {"p": p(94.500,  22.063), "degree": 0,   "flip": False},  # M2 Spacer Hole
        "SH4":   {"p": p(61.660,  61.870), "degree": 0,   "flip": False},  # M2 Spacer Hole
        "SH5":   {"p": p(108.220, 69.480), "degree": 0,   "flip": False},  # M2 Spacer Hole
        "TH1":   {"p": p(116.760, 54.600), "degree": 0,   "flip": False},  # M2 Thread Hole
        "TH2":   {"p": p(131.190, 63.120), "degree": 0,   "flip": False},  # M2 Thread Hole
        "RSW1":  {"p": p(131.315, 46.875), "degree": 270, "flip": False},
        "SW1":   {"p": p(9.000,   16.125), "degree": 0,   "flip": False},
        "SW2":   {"p": p(28.000,  16.125), "degree": 0,   "flip": False},
        "SW3":   {"p": p(47.000,  11.375), "degree": 0,   "flip": False},
        "SW4":   {"p": p(66.000,   9.000), "degree": 0,   "flip": False},
        "SW5":   {"p": p(85.000,  11.375), "degree": 0,   "flip": False},
        "SW6":   {"p": p(104.000, 13.750), "degree": 0,   "flip": False},
        "SW7":   {"p": p(9.000,   35.125), "degree": 0,   "flip": False},
        "SW8":   {"p": p(28.000,  35.125), "degree": 0,   "flip": False},
        "SW9":   {"p": p(47.000,  30.375), "degree": 0,   "flip": False},
        "SW10":  {"p": p(66.000,  28.000), "degree": 0,   "flip": False},
        "SW11":  {"p": p(85.000,  30.375), "degree": 0,   "flip": False},
        "SW12":  {"p": p(104.000, 32.750), "degree": 0,   "flip": False},
        "SW13":  {"p": p(9.000,   54.125), "degree": 0,   "flip": False},
        "SW14":  {"p": p(28.000,  54.125), "degree": 0,   "flip": False},
        "SW15":  {"p": p(47.000,  49.375), "degree": 0,   "flip": False},
        "SW16":  {"p": p(66.000,  47.000), "degree": 0,   "flip": False},
        "SW17":  {"p": p(85.000,  49.375), "degree": 0,   "flip": False},
        "SW18":  {"p": p(104.000, 51.750), "degree": 0,   "flip": False},
        "SW19":  {"p": p(75.500,  69.000), "degree": 0,   "flip": False},
        "SW20":  {"p": p(96.5000, 71.750), "degree": 345, "flip": False},
        "SW21":  {"p": p(118.750, 75.500), "degree": 60,  "flip": False},
        "D1":    {"p": p(16.500,  16.125), "degree": 90,  "flip": True},
        "D2":    {"p": p(35.500,  16.125), "degree": 90,  "flip": True},
        "D3":    {"p": p(54.375,  11.375), "degree": 90,  "flip": True},
        "D4":    {"p": p(73.375,   9.000), "degree": 90,  "flip": True},
        "D5":    {"p": p(92.375,  11.375), "degree": 90,  "flip": True},
        "D6":    {"p": p(111.500, 13.750), "degree": 90,  "flip": True},
        "D7":    {"p": p(16.500,  35.125), "degree": 90,  "flip": True},
        "D8":    {"p": p(35.500,  35.125), "degree": 90,  "flip": True},
        "D9":    {"p": p(54.375,  30.375), "degree": 90,  "flip": True},
        "D10":   {"p": p(73.375,  28.000), "degree": 90,  "flip": True},
        "D11":   {"p": p(92.375,  30.375), "degree": 90,  "flip": True},
        "D12":   {"p": p(111.500, 32.750), "degree": 90,  "flip": True},
        "D13":   {"p": p(16.500,  54.125), "degree": 90,  "flip": True},
        "D14":   {"p": p(35.500,  54.125), "degree": 90,  "flip": True},
        "D15":   {"p": p(54.375,  49.375), "degree": 90,  "flip": True},
        "D16":   {"p": p(73.375,  47.000), "degree": 90,  "flip": True},
        "D17":   {"p": p(92.375,  49.375), "degree": 90,  "flip": True},
        "D18":   {"p": p(111.500, 51.750), "degree": 90,  "flip": True},
        "D19":   {"p": p(65.000,  69.000), "degree": 90,  "flip": True},
        "D20":   {"p": p(84.000,  69.000), "degree": 90,  "flip": True},
        "D21":   {"p": p(87.000,  69.000), "degree": 90,  "flip": True},
        "LED1":  {"p": p(28.000,  25.625), "degree": 180, "flip": True},  # WS2812B
        "LED2":  {"p": p(66.000,  18.500), "degree": 180, "flip": True},  # WS2812B
        "LED3":  {"p": p(104.000, 23.250), "degree": 180, "flip": True},  # WS2812B
        "LED4":  {"p": p(28.000,  44.625), "degree": 180, "flip": True},  # WS2812B
        "LED5":  {"p": p(66.000,  56.500), "degree": 180, "flip": True},  # WS2812B
        "LED6":  {"p": p(104.000, 61.250), "degree": 180, "flip": True},  # WS2812B
        "LED7":  {"p": p(9.000,   20.875), "degree": 0,   "flip": True},
        "LED8":  {"p": p(28.000,  20.875), "degree": 0,   "flip": True},
        "LED9":  {"p": p(47.000,  16.125), "degree": 0,   "flip": True},
        "LED10": {"p": p(66.000,  13.750), "degree": 0,   "flip": True},
        "LED11": {"p": p(85.000,  16.125), "degree": 0,   "flip": True},
        "LED12": {"p": p(104.000, 18.500), "degree": 0,   "flip": True},
        "LED13": {"p": p(9.000,   39.875), "degree": 0,   "flip": True},
        "LED14": {"p": p(28.000,  39.875), "degree": 0,   "flip": True},
        "LED15": {"p": p(47.000,  35.125), "degree": 0,   "flip": True},
        "LED16": {"p": p(66.000,  32.750), "degree": 0,   "flip": True},
        "LED17": {"p": p(85.000,  35.125), "degree": 0,   "flip": True},
        "LED18": {"p": p(104.000, 37.500), "degree": 0,   "flip": True},
        "LED19": {"p": p(9.000,   58.875), "degree": 0,   "flip": True},
        "LED20": {"p": p(28.000,  58.875), "degree": 0,   "flip": True},
        "LED21": {"p": p(47.000,  54.125), "degree": 0,   "flip": True},
        "LED22": {"p": p(66.000,  51.750), "degree": 0,   "flip": True},
        "LED23": {"p": p(85.000,  54.125), "degree": 0,   "flip": True},
        "LED24": {"p": p(104.000, 56.500), "degree": 0,   "flip": True},
        "LED25": {"p": p(75.500,  73.750), "degree": 0,   "flip": True},
        "LED26": {"p": p(95.270,  76.340), "degree": 345, "flip": True},
        "LED27": {"p": p(122.865, 77.875), "degree": 60,  "flip": True},
        "LOGO1": {"p": p(47.000,  61.385), "degree": 0,   "flip": False},
        "LOGO2": {"p": p(46.790,  61.385), "degree": 180, "flip": True},
        "BT1":   {"p": p(9.000,   6.925),  "degree": 0,   "flip": False},  # Break Away Tab
        "BT2":   {"p": p(123.705, 6.925),  "degree": 0,   "flip": False},  # Break Away Tab
        "BT3":   {"p": p(9.000,   63.325), "degree": 0,   "flip": False},  # Break Away Tab
        "BT4":   {"p": p(47.000,  63.325), "degree": 0,   "flip": False},  # Break Away Tab
        # right
        "U2":    {"p": p(150.795, 26.765), "degree": 0,   "flip": False},  # Pro Micro
        "J3":    {"p": p(141.430, 54.635), "degree": 90,  "flip": False},  # TRRS Jack
        "J4":    {"p": p(147.070, 47.373), "degree": 0,   "flip": False},  # OLED Jack
        "SH6":   {"p": p(256.000, 25.625), "degree": 0,   "flip": False},  # M2 Spacer Hole
        "SH7":   {"p": p(256.000, 44.625), "degree": 0,   "flip": False},  # M2 Spacer Hole
        "SH8":   {"p": p(180.000, 22.063), "degree": 0,   "flip": False},  # M2 Spacer Hole
        "SH9":   {"p": p(212.840, 61.870), "degree": 0,   "flip": False},  # M2 Spacer Hole
        "SH10":  {"p": p(166.280, 69.480), "degree": 0,   "flip": False},  # M2 Spacer Hole
        "TH3":   {"p": p(157.740, 54.600), "degree": 0,   "flip": False},  # M2 Thread Hole
        "TH4":   {"p": p(143.310,  63.12), "degree": 0,   "flip": False},  # M2 Thread Hole
        "RSW2":  {"p": p(143.195, 46.875), "degree": 270, "flip": False},
        "SW22":  {"p": p(265.500, 16.125), "degree": 0,   "flip": False},
        "SW23":  {"p": p(246.500, 16.125), "degree": 0,   "flip": False},
        "SW24":  {"p": p(227.500, 11.375), "degree": 0,   "flip": False},
        "SW25":  {"p": p(208.500,  9.000), "degree": 0,   "flip": False},
        "SW26":  {"p": p(189.500, 11.375), "degree": 0,   "flip": False},
        "SW27":  {"p": p(170.500, 13.750), "degree": 0,   "flip": False},
        "SW28":  {"p": p(265.500, 35.125), "degree": 0,   "flip": False},
        "SW29":  {"p": p(246.500, 35.125), "degree": 0,   "flip": False},
        "SW30":  {"p": p(227.500, 30.375), "degree": 0,   "flip": False},
        "SW31":  {"p": p(208.500, 28.000), "degree": 0,   "flip": False},
        "SW32":  {"p": p(189.500, 30.375), "degree": 0,   "flip": False},
        "SW33":  {"p": p(170.500, 32.750), "degree": 0,   "flip": False},
        "SW34":  {"p": p(265.500, 54.125), "degree": 0,   "flip": False},
        "SW35":  {"p": p(246.500, 54.125), "degree": 0,   "flip": False},
        "SW36":  {"p": p(227.500, 49.375), "degree": 0,   "flip": False},
        "SW37":  {"p": p(208.500, 47.000), "degree": 0,   "flip": False},
        "SW38":  {"p": p(189.500, 49.375), "degree": 0,   "flip": False},
        "SW39":  {"p": p(170.500, 51.750), "degree": 0,   "flip": False},
        "SW40":  {"p": p(199.000, 69.000), "degree": 0,   "flip": False},
        "SW41":  {"p": p(178.000, 71.750), "degree": 15,  "flip": False},
        "SW42":  {"p": p(155.750, 75.500), "degree": 300, "flip": False},
        "D22":   {"p": p(273.000, 16.125), "degree": 90,  "flip": True},
        "D23":   {"p": p(254.000, 16.125), "degree": 90,  "flip": True},
        "D24":   {"p": p(235.125, 11.375), "degree": 90,  "flip": True},
        "D25":   {"p": p(216.125,  9.000), "degree": 90,  "flip": True},
        "D26":   {"p": p(197.125, 11.375), "degree": 90,  "flip": True},
        "D27":   {"p": p(178.000, 13.750), "degree": 90,  "flip": True},
        "D28":   {"p": p(273.000, 35.125), "degree": 90,  "flip": True},
        "D29":   {"p": p(254.000, 35.125), "degree": 90,  "flip": True},
        "D30":   {"p": p(235.125, 30.375), "degree": 90,  "flip": True},
        "D31":   {"p": p(216.125, 28.000), "degree": 90,  "flip": True},
        "D32":   {"p": p(197.125, 30.375), "degree": 90,  "flip": True},
        "D33":   {"p": p(178.000, 32.750), "degree": 90,  "flip": True},
        "D34":   {"p": p(273.000, 54.125), "degree": 90,  "flip": True},
        "D35":   {"p": p(254.000, 54.125), "degree": 90,  "flip": True},
        "D36":   {"p": p(235.125, 49.375), "degree": 90,  "flip": True},
        "D37":   {"p": p(216.125, 47.000), "degree": 90,  "flip": True},
        "D38":   {"p": p(197.125, 49.375), "degree": 90,  "flip": True},
        "D39":   {"p": p(178.000, 51.750), "degree": 90,  "flip": True},
        "D40":   {"p": p(206.500, 69.000), "degree": 90,  "flip": True},
        "D41":   {"p": p(188.500, 69.000), "degree": 90,  "flip": True},
        "D42":   {"p": p(185.500, 69.000), "degree": 90,  "flip": True},
        "LED28": {"p": p(246.500, 25.625), "degree": 180, "flip": True},  # WS2812B
        "LED29": {"p": p(208.500, 18.500), "degree": 180, "flip": True},  # WS2812B
        "LED30": {"p": p(170.500, 23.250), "degree": 180, "flip": True},  # WS2812B
        "LED31": {"p": p(246.500, 44.625), "degree": 180, "flip": True},  # WS2812B
        "LED32": {"p": p(208.500, 56.500), "degree": 180, "flip": True},  # WS2812B
        "LED33": {"p": p(170.500, 61.250), "degree": 180, "flip": True},  # WS2812B
        "LED34": {"p": p(265.500, 20.875), "degree": 0,   "flip": True},
        "LED35": {"p": p(246.500, 20.875), "degree": 0,   "flip": True},
        "LED36": {"p": p(227.500, 16.125), "degree": 0,   "flip": True},
        "LED37": {"p": p(208.500, 13.750), "degree": 0,   "flip": True},
        "LED38": {"p": p(189.500, 16.125), "degree": 0,   "flip": True},
        "LED39": {"p": p(170.500, 18.500), "degree": 0,   "flip": True},
        "LED40": {"p": p(265.500, 39.875), "degree": 0,   "flip": True},
        "LED41": {"p": p(246.500, 39.875), "degree": 0,   "flip": True},
        "LED42": {"p": p(227.500, 35.125), "degree": 0,   "flip": True},
        "LED43": {"p": p(208.500, 32.750), "degree": 0,   "flip": True},
        "LED44": {"p": p(189.500, 35.125), "degree": 0,   "flip": True},
        "LED45": {"p": p(170.500, 37.500), "degree": 0,   "flip": True},
        "LED46": {"p": p(265.500, 58.875), "degree": 0,   "flip": True},
        "LED47": {"p": p(246.500, 58.875), "degree": 0,   "flip": True},
        "LED48": {"p": p(227.500, 54.125), "degree": 0,   "flip": True},
        "LED49": {"p": p(208.500, 51.750), "degree": 0,   "flip": True},
        "LED50": {"p": p(189.500, 54.125), "degree": 0,   "flip": True},
        "LED51": {"p": p(170.500, 56.500), "degree": 0,   "flip": True},
        "LED52": {"p": p(199.000, 73.750), "degree": 0,   "flip": True},
        "LED53": {"p": p(179.235, 76.340), "degree": 15,  "flip": True},
        "LED54": {"p": p(151.645, 77.875), "degree": 300, "flip": True},
        "LOGO3": {"p": p(227.460, 61.385), "degree": 0,   "flip": False},
        "LOGO4": {"p": p(227.250, 61.385), "degree": 180, "flip": True},
        "BT5":   {"p": p(150.795,  6.925), "degree": 0,   "flip": False},  # Break Away Tab
        "BT6":   {"p": p(265.5,    6.925), "degree": 0,   "flip": False},  # Break Away Tab
        "BT7":   {"p": p(227.5,   63.325), "degree": 0,   "flip": False},  # Break Away Tab
        "BT8":   {"p": p(265.5,   63.325), "degree": 0,   "flip": False},  # Break Away Tab
    }.items():
        module = pcb.FindModuleByReference(ref)
        if (module.IsFlipped() and not m["flip"]) or (not module.IsFlipped() and m["flip"]):
            module.Flip(module.GetPosition())
        module.SetPosition(m["p"])
        module.SetOrientation(m["degree"] * 10.0)
    pcbnew.Refresh()

def draw_corne_track():
    pcb = pcbnew.GetBoard()

    # draw switch to diode
    for ref in [
        "SW1", "SW2", "SW3", "SW4", "SW5", "SW6", "SW7", "SW8", "SW9", "SW10", "SW11", "SW12", "SW13", "SW14", "SW15", "SW16", "SW17", "SW18",
        "SW22", "SW23", "SW24", "SW25", "SW26", "SW27", "SW28", "SW29", "SW30", "SW31", "SW32", "SW33", "SW34", "SW35", "SW36", "SW37", "SW38", "SW39"
    ]:
        module = pcb.FindModuleByReference(ref)
        psw = module.GetPosition()
        draw_tracks([
            {"p": mp(psw, 5.85, -5.125), "r": 0.0},
            {"p": mp(psw, 7.50, -5.125), "r": 1.0},
            {"p": mp(psw, 7.50, -1.875), "r": 0.0}
        ], p(0, 0), pcbnew.B_Cu)

    pcbnew.Refresh()

def run():
    draw_corne_edge_cuts()
    set_corne_footprints()
    pcbnew.Refresh()
    pcb = pcbnew.GetBoard()
    pcb.Save(pcb.GetFileName())
