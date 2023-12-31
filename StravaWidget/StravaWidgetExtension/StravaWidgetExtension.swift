//
//  StravaWidgetExtension.swift
//  StravaWidgetExtension
//
//  Created by Jacob Kerstetter on 12/4/23.
//

import WidgetKit
import SwiftUI

struct Provider: TimelineProvider {
    
    let data = ReadData()
    
    func placeholder(in context: Context) -> SimpleEntry {
        SimpleEntry(date: Date(),
                    activityName: data.getName(),
                    activityDistance: data.getDistance(),
                    activityTime: data.getTime())
    }

    func getSnapshot(in context: Context, completion: @escaping (SimpleEntry) -> ()) {
        let entry = SimpleEntry(date: Date(),
                                activityName: data.getName(),
                                activityDistance: data.getDistance(),
                                activityTime: data.getTime())
        completion(entry)
    }

    func getTimeline(in context: Context, completion: @escaping (Timeline<Entry>) -> ()) {
        var entries: [SimpleEntry] = []

        // Generate a timeline consisting of five entries an hour apart, starting from the current date.
        let currentDate = Date()
        for hourOffset in 0 ..< 5 {
            let entryDate = Calendar.current.date(byAdding: .hour, value: hourOffset, to: currentDate)!
            let entry = SimpleEntry(date: Date(),
                                    activityName: data.getName(),
                                    activityDistance: data.getDistance(),
                                    activityTime: data.getTime())
            entries.append(entry)
        }

        let timeline = Timeline(entries: entries, policy: .atEnd)
        completion(timeline)
    }
}

struct SimpleEntry: TimelineEntry {
    let date: Date
    let activityName: String
    let activityDistance: String
    let activityTime: String
}

struct StravaWidgetExtensionEntryView : View {
    var entry: Provider.Entry
    
    var body: some View {
        VStack {
            HStack {
                //Image(.strava)
//                    .resizable()
//                    .frame(width: 25.0, height: 25.0, alignment: .center)
//                    .padding(5)
                Text("Strava Widget")
                    .font(.system(size: 18, weight: .black))
                    .foregroundColor(Color(red: 0x00, green: 0x00, blue: 0x00))
                    .multilineTextAlignment(.center)
            }.frame(maxWidth: 170, maxHeight: .infinity)
            HStack {
                Image(.shoe)
                    .resizable()
                    .frame(width: 20.0, height: 20.0, alignment: .leading)
                    .padding(.leading, 7)
                Text("Activity: " + entry.activityName)
                    .font(.system(size: 12, weight: .bold))
                    .frame(alignment: .center)
                Spacer()
            }.frame(maxWidth: 170)
            HStack {
                Image(.road)
                    .resizable()
                    .frame(width: 20.0, height: 20.0, alignment: .leading)
                    .padding(.leading, 7)
                Text("Distance: " + entry.activityDistance)
                    .font(.system(size: 12, weight: .bold))
                    .frame(alignment: .center)
                Spacer()
            }.frame(maxWidth: 170)
            HStack {
                Image(.clock)
                    .resizable()
                    .frame(width: 20.0, height: 20.0, alignment: .leading)
                    .padding([.bottom, .leading], 7)
                Text("Time: " + entry.activityTime)
                    .font(.system(size: 12, weight: .bold))
                    .frame(alignment: .center)
                Spacer()
            }.frame(maxWidth: 170)
        }
        .padding([.bottom], 5)
        .frame(maxWidth: .infinity, maxHeight: .infinity, alignment: .bottom)
        .background(Color("backgroundColor"))
    }
}

struct StravaWidgetExtension: Widget {
    let kind: String = "StravaWidgetExtension"

    var body: some WidgetConfiguration {
        StaticConfiguration(kind: kind, provider: Provider()) { entry in
            if #available(iOS 17.0, *) {
                StravaWidgetExtensionEntryView(entry: entry)
            } else {
                StravaWidgetExtensionEntryView(entry: entry)
            }
        }
        .configurationDisplayName("My Widget")
        .description("This is an example widget.")
        .contentMarginsDisabled()
    }
}

#Preview(as: .systemSmall) {
    StravaWidgetExtension()
} timeline: {
    SimpleEntry(date: .now, activityName: "Test", activityDistance: "0.0", activityTime: "00:00")
}
