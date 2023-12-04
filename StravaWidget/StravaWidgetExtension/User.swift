//
//  User.swift
//  StravaWidget
//
//  Created by Jacob Kerstetter on 12/4/23.
//

import Foundation
import SwiftUI

struct User: Codable, Identifiable {
    enum CodingKeys: CodingKey {
        case mileage
        case designation
        case email
    }
    
    var id = UUID()
    var mileage: String
    var designation: String
    var email: String
}

class ReadData: ObservableObject  {
    @Published var users = [User]()
    
    init(){
        loadData()
    }
    
    func loadData()  {
        guard let url = Bundle.main.url(forResource: "userdata", withExtension: "json")
        else {
            print("Json file not found")
            return
        }
        
        let data = try? Data(contentsOf: url)
        let users = try? JSONDecoder().decode([User].self, from: data!)
        self.users = users!
    }
    
    func getMileage() -> String {
        return self.users[0].mileage
    }
}
