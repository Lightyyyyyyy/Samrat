from vehicle_counting import VehicleCounter

road_D = VehicleCounter("D", r"C:\\Users\\user\\OneDrive\\Desktop\\feed\\Feed 4.mp4")
road_D.process_video()
print(f"Total unique vehicles detected on Road D: {road_D.get_vehicle_count()}")