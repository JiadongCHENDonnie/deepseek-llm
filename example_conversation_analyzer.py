#!/usr/bin/env python3
"""
Example: Using Conversation Analyzer with DeepSeek LLM

This example demonstrates how to integrate the Conversation Analyzer
with DeepSeek LLM to improve user interactions.
"""

from conversation_analyzer import ConversationAnalyzer


def demonstrate_basic_usage():
    """Demonstrate basic conversation analysis."""
    print("=" * 70)
    print("EXAMPLE 1: Basic Conversation Analysis")
    print("=" * 70)
    
    analyzer = ConversationAnalyzer()
    
    # Example text with issues
    text = "hey! can u help me with this problem? its urgent and i need 2 know asap"
    
    print(f"\nOriginal text:\n  \"{text}\"\n")
    
    # Get analysis
    analysis = analyzer.analyze_conversation(text)
    
    # Show recommendations
    print("Quick Recommendations:")
    for i, rec in enumerate(analysis['recommendations'], 1):
        print(f"  {i}. {rec}")
    
    print()


def demonstrate_mixed_language():
    """Demonstrate mixed language detection."""
    print("=" * 70)
    print("EXAMPLE 2: Mixed Language Detection")
    print("=" * 70)
    
    analyzer = ConversationAnalyzer()
    
    # Example with mixed languages
    text = "I want to learn 我想学习 programming and AI technology."
    
    print(f"\nText with mixed languages:\n  \"{text}\"\n")
    
    # Get full report
    report = analyzer.self_review_report(text)
    print(report)


def demonstrate_improvement_workflow():
    """Demonstrate how to use the analyzer for self-improvement."""
    print("=" * 70)
    print("EXAMPLE 3: Self-Improvement Workflow")
    print("=" * 70)
    
    analyzer = ConversationAnalyzer()
    
    # Original message
    original = "can u pls help me? i want 2 learn AI but dont know where 2 start"
    
    print(f"\nOriginal message:\n  \"{original}\"\n")
    
    # Analyze original
    analysis1 = analyzer.analyze_conversation(original)
    print("Issues found:")
    for rec in analysis1['recommendations']:
        print(f"  • {rec}")
    
    # Improved version
    improved = "Can you please help me? I want to learn AI but don't know where to start."
    
    print(f"\nImproved message:\n  \"{improved}\"\n")
    
    # Analyze improved
    analysis2 = analyzer.analyze_conversation(improved)
    print("After improvement:")
    for rec in analysis2['recommendations']:
        print(f"  • {rec}")
    
    print()


def demonstrate_conversation_comparison():
    """Compare multiple conversation styles."""
    print("=" * 70)
    print("EXAMPLE 4: Comparing Different Communication Styles")
    print("=" * 70)
    
    analyzer = ConversationAnalyzer()
    
    conversations = [
        ("Informal", "hey whats up? u free 2 talk? need ur help asap thx"),
        ("Mixed", "Hello! 你好！I need help with my project. 可以帮我吗？"),
        ("Formal", "Good morning. I would appreciate your assistance with my project. Thank you."),
    ]
    
    for style, text in conversations:
        print(f"\n{style} Style:")
        print(f"  Text: \"{text}\"")
        
        analysis = analyzer.analyze_conversation(text)
        
        # Show key metrics
        word_stats = analysis['word_statistics']
        mixed = analysis['mixed_language_usage']
        
        print(f"  Total words: {word_stats['total_words']}")
        print(f"  Avg word length: {word_stats['avg_word_length']:.1f}")
        print(f"  Short words: {word_stats['short_words_count']}")
        print(f"  Mixed language: {'Yes' if mixed['is_mixed_language'] else 'No'}")
        print(f"  Issues: {len(analysis['recommendations'])}")
    
    print()


def demonstrate_detailed_analysis():
    """Show detailed analysis results."""
    print("=" * 70)
    print("EXAMPLE 5: Detailed Analysis Results")
    print("=" * 70)
    
    analyzer = ConversationAnalyzer()
    
    text = """Hello everyone! I want 2 share my experience learning AI.
    
Its been challenging but rewarding. i started with Python basics,
then moved to machine learning. Can u believe it took me 6 months?

Now i can build models and understand neural networks 神经网络.
If ur interested in learning, just start! dont wait 4 perfect conditions."""
    
    print(f"\nAnalyzing multi-paragraph text...\n")
    
    analysis = analyzer.analyze_conversation(text)
    
    print("=== Language Distribution ===")
    for lang, pct in analysis['language_distribution'].items():
        if pct > 0:
            print(f"  {lang.capitalize()}: {pct:.1f}%")
    
    print("\n=== Word Statistics ===")
    ws = analysis['word_statistics']
    print(f"  Total words: {ws['total_words']}")
    print(f"  Unique words: {ws['unique_words']}")
    print(f"  Average word length: {ws['avg_word_length']:.2f}")
    print(f"  Short/informal words: {ws['short_words_count']}")
    if ws.get('short_words_used'):
        print(f"  Short words found: {', '.join(ws['short_words_used'])}")
    
    print("\n=== Grammar Insights ===")
    gi = analysis['grammar_insights']
    print(f"  Total sentences: {gi['sentence_count']}")
    print(f"  Avg words/sentence: {gi['avg_sentence_length']:.1f}")
    print(f"  Capitalization issues: {gi['capitalization_issues']}")
    print(f"  Punctuation issues: {gi['missing_punctuation']}")
    
    print("\n=== Mixed Language Analysis ===")
    ml = analysis['mixed_language_usage']
    print(f"  Uses mixed languages: {'Yes' if ml['is_mixed_language'] else 'No'}")
    print(f"  Mixed sentences: {ml['mixed_sentence_count']} / {ml['total_sentences']}")
    print(f"  Mixing percentage: {ml['mixing_percentage']:.1f}%")
    
    print("\n=== Recommendations ===")
    for i, rec in enumerate(analysis['recommendations'], 1):
        print(f"  {i}. {rec}")
    
    print()


def main():
    """Run all examples."""
    print("\n")
    print("#" * 70)
    print("# CONVERSATION ANALYZER - USAGE EXAMPLES")
    print("#" * 70)
    print()
    
    examples = [
        demonstrate_basic_usage,
        demonstrate_mixed_language,
        demonstrate_improvement_workflow,
        demonstrate_conversation_comparison,
        demonstrate_detailed_analysis,
    ]
    
    for example in examples:
        example()
        input("Press Enter to continue to next example...")
        print("\n")
    
    print("=" * 70)
    print("All examples completed!")
    print("=" * 70)
    print("\nTry it yourself:")
    print('  python conversation_analyzer.py "Your text here"')
    print("\nOr import it in your code:")
    print("  from conversation_analyzer import ConversationAnalyzer")
    print()


if __name__ == "__main__":
    main()
