
from flask import Flask,render_template,request,url_for,redirect,session
from category_list import category_list,sub_cat_list,product_type_list,result_function,bg_func,extended_result_function,comp_logo

cat_list=category_list()

app = Flask(__name__)
app.config["SECRET_KEY"] = "adecf8e7745aca34155ded7c8b787742"

@app.route("/",methods=["GET","POST"])
def login_page():
    if request.method == "POST":
        user_name = request.form["user_id"]
        password = request.form["password"]
        print(user_name,password)
        if user_name == "pankaj" and password == "growth_mate":
            return redirect(url_for("intro_page"))
        else:
            return render_template("login_page.html")
    return render_template("login_page.html")


@app.route("/intro_page",methods=["GET","POST"])
def intro_page():
    if request.method == "POST":
        return redirect(url_for("category_form"))
    return render_template("intro.html")



@app.route("/category_form",methods=["GET","POST"])
def category_form():
    if request.method == "POST":
        category_input_list = request.form.getlist("checkbox_1")
        session["category_input_list"]=category_input_list
        return redirect(url_for("sub_category"))
    return render_template("category.html",posts=cat_list)

@app.route("/sub_category",methods=["GET","POST"])
def sub_category():
    if request.method == "POST":
        sub_cat_input_list = request.form.getlist("checkbox_1")
        session["sub_cat_input_list"] = sub_cat_input_list
        return redirect(url_for("product_type"))

    else:
        if "category_input_list" in session:
            category_input_list = session["category_input_list"]
            sub_cat=sub_cat_list(category_input_list)
            return render_template("sub_category.html",posts=sub_cat)

@app.route("/product_type",methods=["GET","POST"])
def product_type():
    if request.method=="POST":
        product_type_input_list=request.form.getlist("checkbox_1")
        session["product_type_input_list"] = product_type_input_list
        return redirect(url_for("result"))

    else:
        if "sub_cat_input_list" in session:
            sub_cat_input_list = session["sub_cat_input_list"]
            pro_type= product_type_list(sub_cat_input_list)
            return render_template("product_type.html",posts=pro_type)

@app.route("/result",methods=["GET","POST"])
def result():
    if request.method == "POST":
        selected_retailer = request.form.get("discover_more")
        session["selected_retailer"]=selected_retailer
        return redirect(url_for("last_page"))
    else:
        if ("category_input_list" in session) and ("sub_cat_input_list" in session) and ("product_type_input_list" in session):
            category_input_list=session["category_input_list"]
            sub_cat_input_list = session["sub_cat_input_list"]
            product_type_input_list = session["product_type_input_list"]
            result,top_8_dict = result_function(category_input_list,sub_cat_input_list,product_type_input_list)
            return render_template("result.html",result=result,posts=top_8_dict)

@app.route("/last_page",methods=["GET","POST"])
def last_page():
    selected_retailer=session["selected_retailer"]
    category_input_list = session["category_input_list"]
    sub_cat_input_list = session["sub_cat_input_list"]
    product_type_input_list = session["product_type_input_list"]
    background_image=bg_func(selected_retailer)
    result,top_8_dict=extended_result_function(category_input_list,sub_cat_input_list,product_type_input_list,selected_retailer)
    est,local=comp_logo(selected_retailer,category_input_list,sub_cat_input_list)
    return render_template("last_page.html",bg=background_image,post=top_8_dict,est=est,local=local)

if __name__ == '__main__':
    app.debug=True
    app.run()