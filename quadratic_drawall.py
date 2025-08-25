import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from sympy import Eq, Rational, latex, init_printing, sqrt
from sympy.abc import x

init_printing()

st.title("🧮 一元二次方程式求解器")

st.markdown("輸入一元二次方程式係數：形式： ax² + bx + c = 0")

a = Rational(st.number_input("輸入 a（不能為 0）", value=1))
b = Rational(st.number_input("輸入 b", value=0))
c = Rational(st.number_input("輸入 c", value=-2))

if a == 0:
    st.error("這不是一元二次方程式（a 不能為 0）")
else:
    equation = Eq(a * x**2 + b * x + c, 0)
    D = b**2 - 4*a*c
    x_formula = [(-b + sqrt(D)) / (2*a), (-b - sqrt(D)) / (2*a)]

    # 選擇互動方式
    mode = st.selectbox(
        "選擇顯示方式：",
        ["引導步驟版", "一次顯示版"]
    )

    # =============== 引導步驟版（原 Radio） ===============
    if mode == "引導步驟版":
        st.subheader("📖 引導步驟版")
        step = st.radio(
            "選擇要查看的解題步驟：",
            ["步驟 1：寫出方程式",
             "步驟 2：計算判別式 D",
             "步驟 3：判斷根的性質",
             "步驟 4：套用求根公式"]
        )
        if step == "步驟 1：寫出方程式":
            st.latex(latex(equation))
        elif step == "步驟 2：計算判別式 D":
            st.latex(f"D = b^2 - 4ac = ({b})^2 - 4({a})({c}) = {D}")
        elif step == "步驟 3：判斷根的性質":
            if D > 0:
                st.latex("D > 0，因此有兩個相異實數根")
            elif D == 0:
                st.latex("D = 0，因此有一個重根")
            else:
                st.latex("D < 0，因此有兩個共軛虛根")
        elif step == "步驟 4：套用求根公式":
            st.latex(r"x = \frac{-b \pm \sqrt{D}}{2a}")
            for idx, fx in enumerate(x_formula):
                st.latex(f"x_{idx+1} = {latex(fx).replace('I','i')}")

    # =============== 一次顯示版（原 Expander） ===============
    elif mode == "一次顯示版":
        st.subheader("📖 一次顯示版")
        st.markdown("**步驟 1：寫出方程式**")
        st.latex(latex(equation))
        st.markdown("**步驟 2：計算判別式 D**")
        st.latex(f"D = b^2 - 4ac = ({b})^2 - 4({a})({c}) = {D}")
        st.markdown("**步驟 3：判斷根的性質**")
        if D > 0:
            st.latex("D > 0，因此有兩個相異實數根")
        elif D == 0:
            st.latex("D = 0，因此有一個重根")
        else:
            st.latex("D < 0，因此有兩個共軛虛根")
        st.markdown("**步驟 4：套用求根公式**")
        st.latex(r"x = \frac{-b \pm \sqrt{D}}{2a}")
        for idx, fx in enumerate(x_formula):
            st.latex(f"x_{idx+1} = {latex(fx).replace('I','i')}")

    # =============== 是否顯示圖形 ===============
    if st.checkbox("是否顯示函數圖形"):
        st.subheader("📊 拋物線圖示")

        # 頂點座標
        vertex_x = -b / (2*a)
        vertex_y = a*vertex_x**2 + b*vertex_x + c

        # 畫圖範圍
        margin = 2
        if D >= 0:
            roots = [float(r.evalf()) for r in x_formula]
            x_min = min(roots + [float(vertex_x)]) - margin
            x_max = max(roots + [float(vertex_x)]) + margin
        else:
            x_min = float(vertex_x) - 5
            x_max = float(vertex_x) + 5

        xs = np.linspace(x_min, x_max, 400)
        ys = [a*xx**2 + b*xx + c for xx in xs]

        fig, ax = plt.subplots()
        ax.plot(xs, ys, label=f"${latex(equation.lhs)}$")
        ax.axhline(0, color="black", linewidth=1)
        ax.axvline(0, color="gray", linewidth=0.5, linestyle="--")

        # 標記實根
        if D >= 0:
            for r in roots:
                ax.plot(r, 0, "ro", markersize=8)
                ax.text(r, 0, f"{r:.2f}", color="red", ha="center", va="bottom")
        else:
            st.error("⚠️ 此方程式的根為虛數，因此拋物線不與 x 軸相交。")
            st.markdown("### 虛數根：")
            for idx, fx in enumerate(x_formula):
                st.latex(f"x_{idx+1} = {latex(fx).replace('I','i')}")

        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.legend()
        ax.grid(True)

        st.pyplot(fig)
