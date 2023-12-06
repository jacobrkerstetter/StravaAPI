//
//  User.swift
//  StravaWidget
//
//  Created by Jacob Kerstetter on 12/4/23.
//

import Foundation
import SwiftUI

struct Activity: Codable, Identifiable {
    enum CodingKeys: CodingKey {
        case name
        case distance
        case time
    }
    
    var id = UUID()
    var name: String
    var distance: String
    var time: String
}

class ReadData: ObservableObject  {
    @Published var activities = [Activity]()
    
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
        let activities = try? JSONDecoder().decode([Activity].self, from: data!)
        self.activities = activities!
    }
    
    func getName() -> String {
        return self.activities[0].name
    }
    func getDistance() -> String {
        return self.activities[0].distance
    }
    func getTime() -> String {
        return self.activities[0].time
    }
}
