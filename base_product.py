import lumapi

def make_base_fsp(save_path="base.fsp"):
    fdtd = lumapi.FDTD()

    # 尺度参数（按论文描述）
    SI_T   = 220e-9        # Si 厚度 220 nm
    Z_SLAB = 0.0           # 以 Si 薄膜中心为 z=0
    OX_TOP = 2.0e-6        # 上 SiO2 厚度 2 µm
    OX_BOT = 2.0e-6        # 下 SiO2 厚度 2 µm

    # 模拟区域
    X_SPAN = 10e-6
    Y_SPAN = 0.5e-6
    Z_SPAN = 0.22e-6

    cmds = [
        'newproject;',
        # FDTD 区域
        'addfdtd;',
        f'setnamed("FDTD","x span",10e-6);',
        f'setnamed("FDTD","y span",4e-6);',
        f'setnamed("FDTD","z span",5.22e-6);',
        'setnamed("FDTD","mesh accuracy", 2);',
        'setnamed("FDTD","simulation time", 1000e-15);',

        # 边界：全 PML
        'setnamed("FDTD","x min bc","PML");',
        'setnamed("FDTD","x max bc","PML");',
        'setnamed("FDTD","y min bc","PML");',
        'setnamed("FDTD","y max bc","PML");',
        'setnamed("FDTD","z min bc","PML");',
        'setnamed("FDTD","z max bc","PML");',

        # 材料兜底：优先 etch，不存在则 Air，再不行 SiO2
        'mat_hole = "SiO2 (Glass) - Palik";',

        # 下 SiO2 夹层（不与 Si 重叠）
        'addrect; set("name","lower_ox");',
        f'set("z span",{OX_BOT});',
        f'set("z",{- (OX_BOT/2 + SI_T/2)});',
        f'set("x span",{X_SPAN}); set("y span",4e-6);',
        'set("material","SiO2 (Glass) - Palik");',

        # 上 SiO2 夹层
        'addrect; set("name","upper_ox");',
        f'set("z span",{OX_TOP});',
        f'set("z",{(OX_TOP/2 + SI_T/2)});',
        f'set("x span",{X_SPAN}); set("y span",4e-6);',
        'set("material","SiO2 (Glass) - Palik");',
        'setnamed("upper_ox","alpha", 0.05);'
        
        # 中央 Si 薄膜（z=0）
        'addrect; set("name","si_slab");',
        f'set("z span",{SI_T}); set("z",{Z_SLAB});',
        'set("x span", 2.6e-6); set("y span", 2.6e-6);',  # 设计区大小
        'set("material","Si (Silicon) - Palik");',

        # 输入/输出波导（0.5 µm 宽，放在 Si 薄膜层）
        # 输入（左侧）
        'addrect; set("name","input_wg");',
        'set("x", -3.3e-6); set("y", 0);',
        'set("x span", 2e-6); set("y span", 0.5e-6);',
        f'set("z span",{SI_T}); set("z",{Z_SLAB});',
        'set("material","Si (Silicon) - Palik");',

        # 输入锥形 - 从0.5um渐变到1.3um (梯形)'
        'addpoly;',
        'set("name", "input_taper");',
        'set("x", -1.8e-6);',
        'set("y", 0);',
        'set("z", 1e-6 + 110e-9);',
        'set("first axis", "x");',
        'set("vertices", [-0.5e-6, -0.25e-6; -0.5e-6, 0.25e-6; 0.5e-6, 0.65e-6; 0.5e-6, -0.65e-6]);',
        f'set("z span", 220e-9);set("z",{Z_SLAB});',
        'set("material", "Si (Silicon) - Palik");',
        '',

        # 输出（右上/右下）
        'addrect; set("name","output_wg_upper");',
        'set("x",  3.3e-6); set("y",  0.65e-6);',
        'set("x span", 2e-6); set("y span", 0.5e-6);',
        f'set("z span",{SI_T}); set("z",{Z_SLAB});',
        'set("material","Si (Silicon) - Palik");',

        # 上输出锥形 - 从1.3um渐变到0.5um (梯形)'
        'addpoly;',
        'set("name", "output_taper_upper");',
        'set("x", 1.8e-6);',
        'set("y", 0.65e-6);',
        'set("z", 1e-6 + 110e-9);',
        'set("first axis", "x");',
        'set("vertices", [-0.5e-6, -0.65e-6; -0.5e-6, 0.65e-6; 0.5e-6, 0.25e-6; 0.5e-6, -0.25e-6]);',
        f'set("z span", 220e-9);set("z",{Z_SLAB});',
        'set("material", "Si (Silicon) - Palik");',
        '',
        'addrect; set("name","output_wg_lower");',
        'set("x",  3.3e-6); set("y", -0.65e-6);',
        'set("x span", 2e-6); set("y span", 0.5e-6);',
        f'set("z span",{SI_T}); set("z",{Z_SLAB});',
        'set("material","Si (Silicon) - Palik");',

        # 下输出锥形 - 从1.3um渐变到0.5um (梯形)'
        'addpoly;',
        'set("name", "output_taper_lower");',
        'set("x", 1.8e-6);',
        'set("y", -0.65e-6);',
        'set("z", 1e-6 + 110e-9);',
        'set("first axis", "x");',
        'set("vertices", [-0.5e-6, -0.65e-6; -0.5e-6, 0.65e-6; 0.5e-6, 0.25e-6; 0.5e-6, -0.25e-6]);',
        f'set("z span", 220e-9);set("z",{Z_SLAB});',
        'set("material", "Si (Silicon) - Palik");',

        #设置监视器全局变量频率点为21
        'setglobalmonitor("frequency points",21);'
        'setglobalmonitor("wavelength center",1.55e-6);'
        'setglobalmonitor("wavelength span",0.2e-6);'
        
        # 输入端（x=-4um）
        'addpower; set("name","DFT_input");',
        'set("monitor type","2D X-normal");',
        'set("x",-4.0e-6);',
        'set("y", 0.0);', f'set("y span",{Y_SPAN});',
        'set("z", 0.0);', f'set("z span",{Z_SPAN});',

        # 上输出端（x=+4um, y=+0.65um）
        'addpower; set("name","DFT_upper");',
        'set("monitor type","2D X-normal");',
        'set("x", 4.0e-6);',
        'set("y", 0.65e-6);', f'set("y span",{Y_SPAN});',
        'set("z", 0.0);', f'set("z span",{Z_SPAN});',

        # 下输出端（x=+4um, y=-0.65um）
        'addpower; set("name","DFT_lower");',
        'set("monitor type","2D X-normal");',
        'set("x", 4.0e-6);',
        'set("y",-0.65e-6);', f'set("y span",{Y_SPAN});',
        'set("z", 0.0);', f'set("z span",{Z_SPAN});',

        # ========= 宽带脉冲 TE 基模 =========
        # 1550 nm 附近的宽带：1450–1650 nm（脉冲源）
        'addmode; set("name","source"); select("source");',
        'set("injection axis","x"); set("direction","forward");',
        'set("x",-4.2e-6); set("y",0); set("z",0);',
        'set("y span",0.5e-6); set("z span",220e-9);',
        'set("mode selection","fundamental mode");',  # TE-like 基模
        'set("wavelength start",1.45e-6);',
        'set("wavelength stop", 1.65e-6);',  # 宽带 → 脉冲

        # 预留打孔用组
        'addgroup; set("name","hole_array");',

        f'save("{save_path}");',
        '? "base.fsp created";'
    ]

    for i, c in enumerate(cmds, 1):
        if c and not c.strip().startswith('#'):
            fdtd.eval(c)
            if i % 1 == 0:
                print(f"build {i}/{len(cmds)} ...")

if __name__ == "__main__":
    make_base_fsp("base222.fsp")
    print("✅ 基底 base.fsp 已生成")
