from vehicle_counting import VehicleCounter

road_C = VehicleCounter("C", r"C:\\Users\\user\\OneDrive\\Desktop\\feed\\Feed 3.mp4")
road_C.process_video()
print(f"Total unique vehicles detected on Road C: {road_C.get_vehicle_count()}")