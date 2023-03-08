package main

import (
	"encoding/json"
	"github.com/gorilla/mux"
	"log"
	"math/rand"
	"net/http"
	"strconv"
)

type Product struct {
	ID          int    `json:"id"`
	Name        string `json:"name"`
	Description string `json:"description"`
}

var products map[int]Product

func getProducts(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(products)
}

func getProduct(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	id, _ := strconv.Atoi(mux.Vars(r)["id"])
	product, ok := products[id]
	if ok {
		json.NewEncoder(w).Encode(product)
		return
	}
	json.NewEncoder(w).Encode(&Product{})
}

func createProduct(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	var product Product
	_ = json.NewDecoder(r.Body).Decode(&product)
	product.ID = rand.Intn(1000000)
	products[product.ID] = product
	json.NewEncoder(w).Encode(product)
}

func updateProduct(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	id, _ := strconv.Atoi(mux.Vars(r)["id"])
	var product Product
	_ = json.NewDecoder(r.Body).Decode(&product)
	product.ID = id

	products[id] = product
	json.NewEncoder(w).Encode(product)
}

func deleteProduct(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	id, _ := strconv.Atoi(mux.Vars(r)["id"])
	delete(products, id)
	json.NewEncoder(w).Encode(products)
}

func main() {
	r := mux.NewRouter()
	products = make(map[int]Product)
	products[1] = Product{ID: 1, Name: "apple", Description: "fruit"}
	products[2] = Product{ID: 2, Name: "orange", Description: "fruit"}
	r.HandleFunc("/products", getProducts).Methods("GET")
	r.HandleFunc("/products/{id}", getProduct).Methods("GET")
	r.HandleFunc("/products", createProduct).Methods("POST")
	r.HandleFunc("/products/{id}", updateProduct).Methods("PUT")
	r.HandleFunc("/products/{id}", deleteProduct).Methods("DELETE")
	log.Fatal(http.ListenAndServe(":8765", r))
}
