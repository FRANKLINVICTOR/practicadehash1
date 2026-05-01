#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <list>
#include <chrono>
#include <string>

using namespace std;

struct Record {
    string key;
    string value; // Guardaremos el Score de felicidad como string
};

// --- TABLA HASH: ENCADENAMIENTO SEPARADO ---
class HashTableChaining {
private:
    int size;
    vector<list<Record>> table;
    int collisions;

public:
    HashTableChaining(int tableSize) : size(tableSize), collisions(0) {
        table.resize(size);
    }

    int hashFunction(string key) {
        unsigned long hash = 0;
        for (char c : key) hash = hash * 31 + c;
        return hash % size;
    }

    void insert(string key, string value) {
        int index = hashFunction(key);
        if (!table[index].empty()) collisions++;
        table[index].push_back({key, value});
    }

    string search(string key) {
        int index = hashFunction(key);
        for (auto& r : table[index]) {
            if (r.key == key) return r.value;
        }
        return "No encontrado";
    }

    int getCollisions() { return collisions; }
    double loadFactor(int total) { return (double)total / size; }
};

// --- TABLA HASH: SONDEO LINEAL ---
class HashTableLinear {
private:
    int size;
    vector<Record> table;
    vector<bool> occupied;
    int collisions;

public:
    HashTableLinear(int tableSize) : size(tableSize), collisions(0) {
        table.resize(size);
        occupied.resize(size, false);
    }

    int hashFunction(string key) {
        unsigned long hash = 0;
        for (char c : key) hash = hash * 31 + c;
        return hash % size;
    }

    void insert(string key, string value) {
        int index = hashFunction(key);
        while (occupied[index]) {
            collisions++;
            index = (index + 1) % size;
        }
        table[index] = {key, value};
        occupied[index] = true;
    }

    string search(string key) {
        int index = hashFunction(key);
        int start = index;
        while (occupied[index]) {
            if (table[index].key == key) return table[index].value;
            index = (index + 1) % size;
            if (index == start) break;
        }
        return "No encontrado";
    }

    int getCollisions() { return collisions; }
};

// Función para leer el CSV 2019
vector<pair<string, string>> readHappinessCSV(string filename) {
    vector<pair<string, string>> data;
    ifstream file(filename);
    string line, country, score, temp;

    getline(file, line); // Saltar cabecera
    while (getline(file, line)) {
        stringstream ss(line);
        getline(ss, temp, ',');    // Overall rank
        getline(ss, country, ','); // Country or region
        getline(ss, score, ',');   // Score
        data.push_back({country, score});
    }
    return data;
}

int main() {
    string filename = "2019.csv";
    int tableSize = 311;
    auto data = readHappinessCSV(filename);

    HashTableChaining hashChain(tableSize);
    HashTableLinear hashLinear(tableSize);

    // --- PRUEBA ENCADENAMIENTO ---
    auto start = chrono::high_resolution_clock::now();
    for (auto& p : data) hashChain.insert(p.first, p.second);
    auto end = chrono::high_resolution_clock::now();
    chrono::duration<double> t_ins_chain = end - start;

    // --- PRUEBA SONDEO LINEAL ---
    start = chrono::high_resolution_clock::now();
    for (auto& p : data) hashLinear.insert(p.first, p.second);
    end = chrono::high_resolution_clock::now();
    chrono::duration<double> t_ins_linear = end - start;

    // --- SALIDA DE RESULTADOS ---
    cout << "INFORME PRACTICA 3 - C++ (Dataset 2019)" << endl;
    cout << "========================================" << endl;
    cout << "METODO: ENCADENAMIENTO" << endl;
    cout << "Tiempo Insercion: " << t_ins_chain.count() << "s" << endl;
    cout << "Colisiones: " << hashChain.getCollisions() << endl;
    cout << "Factor de Carga: " << hashChain.loadFactor(data.size()) << endl << endl;

    cout << "METODO: SONDEO LINEAL" << endl;
    cout << "Tiempo Insercion: " << t_ins_linear.count() << "s" << endl;
    cout << "Colisiones: " << hashLinear.getCollisions() << endl;

    return 0;
}
