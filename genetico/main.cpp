#include <iostream>
#include <random>
#include <cmath>
#include <ctime>
#include <vector>
#include <map>
#include <tuple>    
#include <fstream>
#include <string>

const int POPULATION_SIZE = 2000;
const int MAX_GEN = 2000;
const float MUTATION_CHANCE = 10;
const float ELITISM = 100;

static std::time_t seed = time(NULL);
static std::mt19937 rng(seed);

//split string
std::vector<std::string> split_string(std::string s, char f){
    std::vector<std::string> ret_vec;

    size_t w_pos = 0;
    while ((w_pos = s.find(f)) != std::string::npos){
        ret_vec.push_back(s.substr(0, w_pos));
        s.erase(0, w_pos+1);
    }
    ret_vec.push_back(s);

    return ret_vec;

}

std::map<int, std::tuple<double, double>> get_nodes_from_file(){
    std::map<int, std::tuple<double, double>> m;

    std::fstream file("berlin52.tsp");

    std::string target;

    //Pula para linha com coordenadas
    for (size_t i = 0; i < 7; i++){
        //file.ignore((unsigned int)-1, '\n');
        std::getline(file, target);
    }

    
    while(target != "EOF"){
        std::vector<std::string> temp = split_string(target, ' ');
        m.insert({std::stoi(temp[0]), std::tuple<double, double>(std::stod(temp[1]), std::stod(temp[2]))});
        std::getline(file, target);
    }

    file.close();
    
    return m;
}



std::vector<int> get_map_keys(std::map<int, std::tuple<double, double>>& nodes){
    std::vector<int> new_vector;
    new_vector.reserve(nodes.size());
    

    for(auto it = nodes.begin(); it != nodes.end(); it++){
        new_vector.push_back(it->first);
    }
    
    return new_vector;
}

std::vector<int> make_random_path(std::vector<int>& route){
    std::vector<int> new_vector(route);
    
    for (size_t i = 0; i < new_vector.size(); i++){
        size_t rand_idx = std::uniform_int_distribution<int>(i, new_vector.size()-1)(rng);
        int temp_var = new_vector[i];
        new_vector[i] = new_vector[rand_idx];
        new_vector[rand_idx] = temp_var;
    }

    return new_vector;
}

void mutate(std::vector<int>& indiv){
    int i = std::uniform_int_distribution<int>(1, indiv.size()-2)(rng);
    int j = std::uniform_int_distribution<int>(i+1, indiv.size()-1)(rng);

    while (i < j){
        int temp = indiv[i];
        indiv[i] = indiv[j];
        indiv[j] = temp; 
        i++;
        j--;
    }
}


std::vector<std::vector<int>> crossover(std::vector<int>& s, std::vector<int>& t){

    std::vector<int> child1(s);
    std::vector<int> child2(t);
    
    int crossover_size = std::uniform_int_distribution<int>(1, s.size())(rng);
    int s_point = std::uniform_int_distribution<int>(0, s.size()-crossover_size)(rng);
    for (size_t i = s_point; i < s_point+crossover_size; i++){
        for (size_t j = 0; j < s.size(); j++){
            if (child1[j] == t[i]){
                int temp = child1[i];
                child1[i] = child1[j];
                child1[j] = temp;
                break;
            }
        }
        for (size_t j = 0; j < s.size(); j++){
            if (child2[j] == s[i]){
                int temp = child2[i];
                child2[i] = child2[j];
                child2[j] = temp;
                break;
            }
        }
    }


    std::vector<std::vector<int>> offspring{child1, child2};
    return offspring;
}

double get_dis(std::tuple<double, double>& a, std::tuple<double, double>& b){
    return std::sqrt(std::pow(std::get<0>(a) - std::get<0>(b), 2) + std::pow(std::get<1>(a) - std::get<1>(b), 2));
}

double get_fit(std::vector<int>& perm, std::map<int, std::tuple<double,double>>& nodes){
    double sum = get_dis(nodes[perm[0]], nodes[perm[perm.size()-1]]);
    //std::cout << sum << "\n";
    for (size_t i = 0; i < perm.size()-1; i++){
        sum += get_dis(nodes[perm[i]], nodes[perm[i+1]]);
    }
    return 1/sum;
}


double get_sum(std::vector<double>& l){
    double sum = 0;
    for (double n: l){
        sum += n;
    }
    return sum;
}


std::vector<size_t> get_chosen(std::vector<double>& population_fit, double fit_sum){
    std::vector<size_t> ret_vec(2, 0);
    double sum = 0;
    double target = std::uniform_real_distribution<double>(0, 1)(rng);
    for (size_t i = 0; i < population_fit.size(); i++){
        sum += population_fit[i]/fit_sum;
        if (target <= sum){
            ret_vec[0] = i;
            break;
        }
    }
    
    double temp = population_fit[ret_vec[0]];
    population_fit[ret_vec[0]] = population_fit[0];
    population_fit[0] = temp;

    sum = 0;
    target = std::uniform_real_distribution<double>(0, 1)(rng);
    for (size_t i = 0; i < population_fit.size(); i++){
        sum += population_fit[i]/fit_sum;
        if (target <= sum){
            ret_vec[1] = i;
            break;
        }
    }

    if (ret_vec[1] == ret_vec[0]){
        ret_vec[1] = 0;
    }

    population_fit[0] = population_fit[ret_vec[0]];
    population_fit[ret_vec[0]] = temp;

    

    return ret_vec;
}


size_t get_max_idx(std::vector<double> l){
    size_t max = 0;
    double max_val = l[0];
    for (size_t i = 1; i < l.size(); i++){
        if (l[i] > max_val){
            max_val = l[i];
            max = i;
        }
    }
    return max;
}

std::tuple<std::vector<int>, double> start(std::map<int, std::tuple<double, double>> nodes){
    std::vector<std::vector<int>> population(POPULATION_SIZE);
    std::vector<int> nodes_keys = get_map_keys(nodes);
    for (size_t i = 0; i < POPULATION_SIZE; i++){
        population[i] = make_random_path(nodes_keys);
    }


    std::vector<double> population_fit(POPULATION_SIZE);

    for (size_t i = 0; i < POPULATION_SIZE; i++){
        population_fit[i] = get_fit(population[i], nodes);
    }

    double fit_sum = get_sum(population_fit);
   
    std::vector<std::vector<int>> new_population(POPULATION_SIZE);
    std::vector<double> new_population_fit(POPULATION_SIZE);

    double all_time_best_fit = 0;
    std::vector<int> all_time_best_route;


    for (size_t k = 0; k < MAX_GEN; k++){
        
        //crossover
        for (size_t i = 0; i < POPULATION_SIZE; i += 2){
            std::vector<size_t> chosen_idx = get_chosen(population_fit, fit_sum);
            std::vector<std::vector<int>> offspring = crossover(population[chosen_idx[0]], population[chosen_idx[1]]);



            //mutation
            if (std::uniform_real_distribution<float>(0, 100)(rng) <= MUTATION_CHANCE){
                mutate(offspring[0]);
            }
            if (std::uniform_real_distribution<float>(0, 100)(rng) <= MUTATION_CHANCE){
                mutate(offspring[1]);
            }



            //filter
            std::vector<double> offspring_fit{get_fit(offspring[0], nodes), get_fit(offspring[1], nodes)};

            for (int j = 0; j < 2; j++){
                if (offspring_fit[j] < population_fit[i+j] && std::uniform_real_distribution<float>(0, 100)(rng) <= ELITISM){
                    new_population[i+j] = population[chosen_idx[j]];
                    new_population_fit[i+j] = population_fit[chosen_idx[j]];
                }else{
                    new_population[i+j] = offspring[j];
                    new_population_fit[i+j] = offspring_fit[j];
                }
            }
            
        }

        population = new_population;
        population_fit = new_population_fit;
        fit_sum = get_sum(population_fit);
        size_t gen_best = get_max_idx(population_fit);
        std::cout << k << "\n";
        std::cout << 1/population_fit[gen_best] << "\n\n";
        if (population_fit[gen_best] > all_time_best_fit){
            all_time_best_fit = population_fit[gen_best];
            all_time_best_route = population[gen_best];
        }
    }

    std::cout << "\n\n" << 1/all_time_best_fit << "\n";
    for (int n: all_time_best_route){
        std::cout << n << " ";
    }
    std::cout << "\n";
    std::cout << seed;

    return std::tuple<std::vector<int>, double>(all_time_best_route, 1/all_time_best_fit);

}


int main(){

    std::map<int, std::tuple<double, double>> nodes = get_nodes_from_file();

    start(nodes);
    //std::cout << std::get<0>(nodes[1]);

    
    return 0;
}