import re
from models.User import User
from models.Style import Style


def parse_time_period(period_str):
    century_match = re.search(r'(\d+)(?:st|nd|rd|th)-(\d+)(?:st|nd|rd|th)', period_str)
    if century_match:
        return {
            'start': int(century_match.group(1)),
            'end': int(century_match.group(2))
        }

    year_match = re.search(r'(\d{4})s?-(\d{4})s?', period_str)
    if year_match:
        import math
        return {
            'start': math.ceil(int(year_match.group(1)) / 100),
            'end': math.ceil(int(year_match.group(2)) / 100)
        }

    single_century_match = re.search(r'(\d+)(?:st|nd|rd|th)', period_str)
    if single_century_match:
        century = int(single_century_match.group(1))
        return {'start': century, 'end': century}

    single_decade_match = re.search(r'(\d{4})s', period_str)
    if single_decade_match:
        import math
        century = math.ceil(int(single_decade_match.group(1)) / 100)
        return {'start': century, 'end': century}

    return {'start': 0, 'end': 0}


def calculate_period_overlap(period1, period2):
    if period1['start'] == 0 or period2['start'] == 0:
        return 0

    has_overlap = (period1['start'] <= period2['end'] and period1['end'] >= period2['start'])

    if not has_overlap:
        gap = min(
            abs(period1['end'] - period2['start']),
            abs(period2['end'] - period1['start'])
        )
        return max(0, 1 - (gap * 0.2))

    overlap_start = max(period1['start'], period2['start'])
    overlap_end = min(period1['end'], period2['end'])
    overlap_length = overlap_end - overlap_start + 1

    period1_length = period1['end'] - period1['start'] + 1
    period2_length = period2['end'] - period2['start'] + 1

    return overlap_length / ((period1_length + period2_length) / 2)


def get_time_based_recommendations(user_id, limit=3, exclude_ids=None):
    if exclude_ids is None:
        exclude_ids = []

    try:
        user = User.query.get(user_id)
        if not user:
            return []

        user_favorites = user.favorites.all()
        if not user_favorites:
            return []

        favorite_ids = [style.id for style in user_favorites]
        all_excluded_ids = list(set(favorite_ids + exclude_ids))

        all_other_styles = Style.query.filter(
            ~Style.id.in_(all_excluded_ids)
        ).all()

        if not all_other_styles:
            return []

        scored_styles = []
        for style in all_other_styles:
            total_score = 0
            style_period = parse_time_period(style.period)

            for fav_style in user_favorites:
                fav_period = parse_time_period(fav_style.period)
                period_overlap = calculate_period_overlap(style_period, fav_period)

                total_score += period_overlap * 3

                if style.characteristics and fav_style.characteristics:
                    common = len(set(style.characteristics) & set(fav_style.characteristics))
                    total_score += common * 0.5

            average_score = total_score / len(user_favorites)
            scored_styles.append({
                'style': style,
                'score': average_score
            })

        scored_styles.sort(key=lambda x: x['score'], reverse=True)
        recommendations = [item['style'] for item in scored_styles[:limit]]

        return recommendations

    except Exception as e:
        print(f'Error getting time-based recommendations: {str(e)}')
        raise


def get_replacement_recommendation(user_id, current_recommendation_ids):
    try:
        recommendations = get_time_based_recommendations(
            user_id,
            1,
            current_recommendation_ids
        )
        return recommendations[0] if recommendations else None

    except Exception as e:
        print(f'Error getting replacement recommendation: {str(e)}')
        raise
