#!/usr/bin/env python3
"""
Tests for the Conversation Analyzer utility.

This module contains basic tests to validate the conversation analysis functionality.
"""

from conversation_analyzer import ConversationAnalyzer


def test_basic_analysis():
    """Test basic conversation analysis."""
    analyzer = ConversationAnalyzer()
    text = "Hello world. This is a test."
    analysis = analyzer.analyze_conversation(text)
    
    assert 'language_distribution' in analysis
    assert 'word_statistics' in analysis
    assert 'grammar_insights' in analysis
    assert 'mixed_language_usage' in analysis
    assert 'recommendations' in analysis
    
    print("✓ Basic analysis test passed")


def test_empty_text():
    """Test handling of empty text."""
    analyzer = ConversationAnalyzer()
    analysis = analyzer.analyze_conversation("")
    
    assert 'error' in analysis
    assert 'recommendations' in analysis
    
    print("✓ Empty text test passed")


def test_language_mixing():
    """Test detection of mixed language usage."""
    analyzer = ConversationAnalyzer()
    text = "This is English 这是中文 mixed together."
    analysis = analyzer.analyze_conversation(text)
    
    assert analysis['mixed_language_usage']['is_mixed_language'] is True
    assert analysis['mixed_language_usage']['mixed_sentence_count'] > 0
    
    print("✓ Language mixing test passed")


def test_short_words_detection():
    """Test detection of short/informal words."""
    analyzer = ConversationAnalyzer()
    text = "Can u help me pls? Thx!"
    analysis = analyzer.analyze_conversation(text)
    
    assert analysis['word_statistics']['short_words_count'] > 0
    assert 'u' in analysis['word_statistics']['short_words_used']
    
    print("✓ Short words detection test passed")


def test_grammar_insights():
    """Test grammar insights analysis."""
    analyzer = ConversationAnalyzer()
    text = "This is sentence one. this is sentence two without capital"
    analysis = analyzer.analyze_conversation(text)
    
    assert analysis['grammar_insights']['sentence_count'] == 2
    assert analysis['grammar_insights']['capitalization_issues'] > 0
    
    print("✓ Grammar insights test passed")


def test_report_generation():
    """Test report generation."""
    analyzer = ConversationAnalyzer()
    text = "Hello world! This is a test."
    report = analyzer.self_review_report(text)
    
    assert isinstance(report, str)
    assert "CONVERSATION SELF-REVIEW REPORT" in report
    assert "Language Distribution:" in report
    assert "Recommendations for Improvement:" in report
    
    print("✓ Report generation test passed")


def test_word_statistics():
    """Test word statistics calculation."""
    analyzer = ConversationAnalyzer()
    text = "one two three four five"
    analysis = analyzer.analyze_conversation(text)
    
    assert analysis['word_statistics']['total_words'] == 5
    assert analysis['word_statistics']['unique_words'] == 5
    assert analysis['word_statistics']['avg_word_length'] > 0
    
    print("✓ Word statistics test passed")


def test_no_language_mixing():
    """Test text without language mixing."""
    analyzer = ConversationAnalyzer()
    text = "This is entirely in English."
    analysis = analyzer.analyze_conversation(text)
    
    assert analysis['mixed_language_usage']['is_mixed_language'] is False
    assert analysis['mixed_language_usage']['mixed_sentence_count'] == 0
    
    print("✓ No language mixing test passed")


def run_all_tests():
    """Run all tests."""
    print("\nRunning Conversation Analyzer Tests...")
    print("=" * 60)
    
    tests = [
        test_basic_analysis,
        test_empty_text,
        test_language_mixing,
        test_short_words_detection,
        test_grammar_insights,
        test_report_generation,
        test_word_statistics,
        test_no_language_mixing,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"✗ {test.__name__} failed: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ {test.__name__} error: {e}")
            failed += 1
    
    print("=" * 60)
    print(f"\nTest Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("All tests passed! ✓")
        return 0
    else:
        print(f"{failed} test(s) failed.")
        return 1


if __name__ == "__main__":
    import sys
    sys.exit(run_all_tests())
