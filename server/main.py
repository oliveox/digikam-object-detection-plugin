from services.utils import Utils
import traceback

if __name__ == "__main__":
    try:
        # start analysis
        Utils.analyze_entities()
    except Exception as e:
        print(f'Analysis failed. Exception: {e}')
        traceback.print_exc()
