import streamlit as st
from sympy import symbols, Eq, solve, Rational, latex, init_printing
from sympy.abc import x

init_printing()

st.title("🧮 一元二次方程式求解器")

st.markdown("輸入一元二次方程式係數：方程式形式： ax² + bx + c = 0")

a = Rational(st.number_input("輸入 a（不能為 0）", value=1))
b = Rational(st.number_input("輸入 b", value=0))
c = Rational(st.number_input("輸入 c", value=-2))

if a == 0:
    st.error("這不是一元二次方程式（a 不能為 0）")
else:
    equation = Eq(a * x**2 + b * x + c, 0)
    st.markdown("### 方程式：")
    st.latex(latex(equation))

    solutions = solve(equation, x)

    # 判別式 D = b^2 - 4ac
    D = b**2 - 4*a*c

    st.markdown("### 判別式 D 計算：")
    st.latex(f"D = b^2 - 4ac = ({b})^2 - 4({a})({c}) = {D}")

    st.markdown("### 根的性質：")
    if D > 0:
        st.success("此方程式有兩個 **相異實數根**。")
    elif D == 0:
        st.info("此方程式有一個 **重根（重複實根）**。")
    else:
        st.warning("此方程式有兩個 **共軛虛根（非實數根）**。")

    # 顯示使用通用公式求解的表示式
    from sympy import sqrt
    x_formula = [(-b + sqrt(D)) / (2*a), (-b - sqrt(D)) / (2*a)]
    st.markdown("### 使用求根公式計算：")
    for idx, fx in enumerate(x_formula):
        latex_fx = latex(fx).replace("I", "i")
        st.latex(f"x_{idx+1} = {latex_fx}")
        