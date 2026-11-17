"""
Grading and performance calculation utilities for the School Results System.
"""
from typing import Optional, Dict, Any, List
from .models import Subject, Result


# Configurable grading scale
# Tuple format: (min_score, max_score, performance_remark, grade_label)
GRADING_SCALE = [
    (80.0, 100.0, "Excellent (Distinction)", "Grade 1"),
    (70.0, 79.99, "Very Good", "Grade 2"),
    (60.0, 69.99, "Good", "Grade 3"),
    (50.0, 59.99, "Credit", "Grade 4"),
    (40.0, 49.99, "Pass", "Grade 5"),
    (0.0, 39.99, "Needs Improvement", "Grade 6"),
]


def get_subject_grade(score: Optional[int]) -> Dict[str, str]:
    """
    Returns remark and grade code for a single subject score.
    """
    if score is None:
        return {"remark": "Pending", "grade": "-"}

    for low, high, remark, grade in GRADING_SCALE:
        if low <= score <= high:
            return {"remark": remark, "grade": grade}

    return {"remark": "Ungraded", "grade": "-"}


def get_overall_performance(average: Optional[float]) -> Optional[Dict[str, str]]:
    """
    Calculates overall performance remark and grade based on the average of all subjects.
    """
    if average is None:
        return None

    for low, high, remark, grade in GRADING_SCALE:
        if low <= average <= high:
            return {"remark": remark, "grade": grade}

    return {"remark": "Ungraded", "grade": "-"}


def get_student_results_summary(student) -> Dict[str, Any]:
    """
    Gathers student results across all subjects and determines completion.
    
    If any subject score has not yet been entered, the system clearly marks
    results as incomplete and does NOT calculate a misleading final average or total.
    """
    subjects: List[Subject] = list(Subject.objects.all().order_by('name'))
    existing_results = {r.subject_id: r for r in Result.objects.filter(student=student)}

    rows = []
    total_score = 0
    entered_count = 0
    total_subjects_count = len(subjects)

    for subj in subjects:
        result_obj = existing_results.get(subj.id)
        if result_obj is not None:
            entered_count += 1
            total_score += result_obj.score
            grade_info = get_subject_grade(result_obj.score)
            rows.append({
                'subject': subj,
                'score': result_obj.score,
                'has_score': True,
                'remark': grade_info['remark'],
                'grade': grade_info['grade'],
                'date_entered': result_obj.date_entered,
            })
        else:
            rows.append({
                'subject': subj,
                'score': None,
                'has_score': False,
                'remark': "Pending",
                'grade': "-",
                'date_entered': None,
            })

    is_complete = (entered_count == total_subjects_count and total_subjects_count > 0)

    if is_complete:
        average_score = round(total_score / total_subjects_count, 2)
        overall_perf = get_overall_performance(average_score)
    else:
        average_score = None
        overall_perf = None

    return {
        'student': student,
        'subjects_count': total_subjects_count,
        'entered_count': entered_count,
        'pending_count': total_subjects_count - entered_count,
        'is_complete': is_complete,
        'rows': rows,
        'total_score': total_score if is_complete else None,
        'max_possible_total': (total_subjects_count * 100) if is_complete else None,
        'average_score': average_score,
        'overall_performance': overall_perf,
    }
