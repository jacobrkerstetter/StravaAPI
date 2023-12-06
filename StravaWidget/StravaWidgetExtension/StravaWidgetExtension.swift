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
                    activityDistance: data.getDistance())
    }

    func getSnapshot(in context: Context, completion: @escaping (SimpleEntry) -> ()) {
        let entry = SimpleEntry(date: Date(),
                                activityName: data.getName(),
                                activityDistance: data.getDistance())
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
                                    activityDistance: data.getDistance())
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
}

struct StravaWidgetExtensionEntryView : View {
    var entry: Provider.Entry

    var body: some View {
        VStack {
            Text("Name:")
            Text(entry.activityName)

            Text("Distance:")
            Text(entry.activityDistance)
        }
    }
}

struct StravaWidgetExtension: Widget {
    let kind: String = "StravaWidgetExtension"

    var body: some WidgetConfiguration {
        StaticConfiguration(kind: kind, provider: Provider()) { entry in
            if #available(iOS 17.0, *) {
                StravaWidgetExtensionEntryView(entry: entry)
                    .containerBackground(.fill.tertiary, for: .widget)
            } else {
                StravaWidgetExtensionEntryView(entry: entry)
                    .padding()
                    .background()
            }
        }
        .configurationDisplayName("My Widget")
        .description("This is an example widget.")
    }
}

#Preview(as: .systemSmall) {
    StravaWidgetExtension()
} timeline: {
    SimpleEntry(date: .now, activityName: "Test", activityDistance: "0.0")
}
