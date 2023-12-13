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
        
        UIFont.familyNames.forEach({ name in
            for font_name in UIFont.fontNames(forFamilyName: name) {
                print("\n\(font_name)")
            }
        })

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
            Text("Recent Activity")
                .font(.custom("Nunito-ExtraBold", fixedSize: 14))
                .padding([.top, .leading], 10)
                .padding([.bottom], 5)
                .frame(alignment: .leading)
                .foregroundColor(.black)
            Spacer()
            HStack {
                Image(.shoe)
                    .resizable()
                    .frame(width: 18.0, height: 18.0, alignment: .leading)
                    .padding([.trailing, .leading], 5)
                Text("Activity: " + entry.activityName)
                    .font(.custom(
                        "Helvetica-Bold",
                    fixedSize: 12))
                    .frame(alignment: .leading)
                Spacer()
            }.frame(maxWidth: .infinity)
            HStack {
                Image(.road)
                    .resizable()
                    .frame(width: 18.0, height: 18.0, alignment: .leading)
                    .padding([.trailing, .leading], 5)
                Text("Distance: " + entry.activityDistance)
                    .font(.custom(
                        "Helvetica-Bold",
                    fixedSize: 12))
                    .frame(alignment: .leading)
                Spacer()
            }.frame(maxWidth: .infinity)
            HStack {
                Image(.clock)
                    .resizable()
                    .frame(width: 18.0, height: 18.0, alignment: .leading)
                    .padding([.trailing, .leading], 5)
                Text("Time: " + entry.activityTime)
                    .font(.custom(
                        "Helvetica-Bold",
                    fixedSize: 12))
                    .frame(alignment: .leading)
                Spacer()
            }.frame(maxWidth: .infinity)
        }
        .padding([.bottom], 5)
        .frame(maxWidth: .infinity, maxHeight: .infinity, alignment: .bottom)
        .background(Color.white)
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
