import pandas as pd

def save_data_to_excel(yt_captions, yt_views, insta_views):
    # Convert views to integers, handling potential conversion issues
    yt_views = [int(view) for view in yt_views]
    insta_views = [int(view) for view in insta_views]

    # Create the primary data sheet
    performance_matrix = [(yt + insta) / 1000 for yt, insta in zip(yt_views, insta_views)]
    top_performing_index = performance_matrix.index(max(performance_matrix))

    # Data for the main sheet
    data = {
        'YouTube Titles': yt_captions,
        'YouTube Views': yt_views,
        'Instagram Reels Views': insta_views,
        'Video Editor': ['XYZ'] * len(yt_captions),
        'Performance Matrix (K)': performance_matrix
    }
    
    df = pd.DataFrame(data)

    # Create a second sheet for the Editors sheet
    top_performing_video = yt_captions[top_performing_index]
    top_views = yt_views[top_performing_index] + insta_views[top_performing_index]

    editor_data = {
        'Name': ['XYZ'],
        'Mobile': ['8990'],
        'Email': ['hbn@yuh.com'],
        'Top Performing Video': [top_performing_video],
        'Views in Top Performing Video': [top_views],
        'Earnings': ['']
    }

    df_editor = pd.DataFrame(editor_data)

    # Save to Excel with two sheets
    with pd.ExcelWriter('social_media_data.xlsx', engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Video Data', index=False)
        df_editor.to_excel(writer, sheet_name='Editors Sheet', index=False)

    print('Data saved to social_media_data.xlsx')
