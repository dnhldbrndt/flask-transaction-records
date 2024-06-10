from  flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)


# Sample data
transactions = [
    {'id': 1, 'date': '2023-03-22', 'amount': 1000},
    {'id': 2, 'date': '2023-05-12', 'amount': -200},
    {'id': 3, 'date': '2023-06-03', 'amount': 350}
]
filtered_transactions = []

# Total Balance
def get_total_balance(transactions):
    balance = 0
    for transaction in transactions:
        balance = balance + transaction['amount']
    return balance
    
    
# Read operation
@app.route("/")
def get_transactions():
    balance = get_total_balance(transactions)
    return render_template("transactions.html", transactions=transactions, balance=balance)
    
    
# Create operation
@app.route("/add", methods=["GET", "POST"])
def add_transaction():
    if request.method == 'POST':
        transaction = {
            'id': len(transactions) + 1,
            'date': request.form['date'],
            'amount': float(request.form['amount'])
        }
        transactions.append(transaction)
        return redirect(url_for("get_transactions"))
    return render_template("form.html")
    
    
# Update operation
@app.route("/edit/<int:transaction_id>", methods=["GET", "POST"])
def edit_transaction(transaction_id):
    if request.method == 'POST':
        date = request.form['date']
        amount = float(request.form['amount'])

        for transaction in transactions:
            if transaction['id'] == transaction_id:
                transaction['date'] = date
                transaction['amount'] = amount
                break
        return redirect(url_for("get_transactions"))
    for transaction in transactions:
        if transaction['id'] == transaction_id:
            return render_template("edit.html", transaction=transaction)
            
            
# Delete operation
@app.route("/delete/<int:transaction_id>")
def delete_transaction(transaction_id):
    for transaction in transactions:
        if transaction['id'] == transaction_id:
            transactions.remove(transaction)
            break
    return redirect(url_for("get_transactions"))
    
    
# Search operation
@app.route("/search", methods= ["GET", "POST"])
def search_transactions():
    if request.method == 'POST':
        minimum = float(request.form['min_amount'])
        maximum = float(request.form['max_amount'])
        for transaction in transactions:
            if transaction['amount'] > minimum and transaction['amount'] < maximum:   
                filtered_transactions.append(transaction)
        balance = get_total_balance(filtered_transactions)
        return render_template("transactions.html", transactions=filtered_transactions, balance=balance)
    if request.method == 'GET':
        return render_template("search.html", transactions=filtered_transactions)
        
        
# Calculate operation
@app.route("/balance")
def total_balance():
    balance = 0
    for transaction in transactions:
        balance += transaction['amount']
    return f"Total Balance: {balance}"
    
    
# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)