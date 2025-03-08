from vehicle_counting import VehicleCounter

road_B = VehicleCounter("B", r"C:\\Users\\user\\OneDrive\\Desktop\\feed\\Feed 2.mp4")
road_B.process_video()
print(f"Total unique vehicles detected on Road B: {road_B.get_vehicle_count()}")